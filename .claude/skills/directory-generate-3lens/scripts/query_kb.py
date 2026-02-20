#!/usr/bin/env python3
"""
KB Query Helper for Three-Lens Directory Generation

Provides structured queries against the NGM Signaling Knowledge Base
for Lens 3 (KB Cross-Referencing).

Usage:
    python query_kb.py --lookup metformin
    python query_kb.py --target AMPK
    python query_kb.py --pathway "mTOR signaling"
    python query_kb.py --indication "glycemic control"
    python query_kb.py --biomarker butyrate           # NEW: for testing products
    python query_kb.py --extract-citations butyrate   # NEW: extract PMIDs/DOIs
    python query_kb.py --full-report metformin
    python query_kb.py --testing-report "microbiome"  # NEW: for diagnostic products
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Configuration
# Script is at .claude/skills/directory-generate-3lens/scripts/query_kb.py
# Need to go up 5 levels to reach project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
KB_ROOT = PROJECT_ROOT / ".signaling-kb"
INTERVENTIONS_DIR = KB_ROOT / "interventions"


def slugify(name: str) -> str:
    """Convert product name to KB slug format."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def load_intervention(slug: str) -> Optional[Dict]:
    """Load an intervention node by slug."""
    path = INTERVENTIONS_DIR / f"{slug}.json"
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None


def list_all_interventions() -> List[str]:
    """List all intervention IDs in the KB."""
    return [f.stem for f in INTERVENTIONS_DIR.glob("*.json")]


def direct_lookup(product_name: str) -> Dict:
    """
    Query Type 1: Direct intervention lookup.

    Tries multiple slug variations to find exact match.
    """
    variations = [
        slugify(product_name),
        slugify(product_name.replace("-", " ")),
        slugify(product_name.replace("_", " ")),
    ]

    # Also try without common suffixes
    for suffix in ["-supplement", "-extract", "-complex"]:
        if product_name.lower().endswith(suffix.replace("-", " ")):
            variations.append(slugify(product_name.lower().replace(suffix.replace("-", " "), "")))

    for slug in variations:
        node = load_intervention(slug)
        if node:
            return {
                "found": True,
                "slug": slug,
                "node_path": str(INTERVENTIONS_DIR / f"{slug}.json"),
                "node": node
            }

    return {
        "found": False,
        "attempted_slugs": variations,
        "node": None
    }


def search_by_target(target: str) -> List[Dict]:
    """
    Query Type 2: Find interventions targeting same molecular target.

    Searches mechanism_claims[].target field.
    """
    matches = []
    target_lower = target.lower()

    # Common aliases
    aliases = {
        "ampk": ["ampk", "prkaa1", "prkaa2", "amp-activated"],
        "mtor": ["mtor", "mtorc1", "mtorc2", "mammalian target"],
        "sirt1": ["sirt1", "sirtuin", "sir2"],
        "nrf2": ["nrf2", "nfe2l2"],
        "pgc1a": ["pgc1a", "pgc-1α", "ppargc1a"],
    }

    search_terms = [target_lower]
    for key, terms in aliases.items():
        if target_lower in terms or key == target_lower:
            search_terms = terms
            break

    for intervention_file in INTERVENTIONS_DIR.glob("*.json"):
        try:
            with open(intervention_file, 'r') as f:
                node = json.load(f)

            for claim in node.get("mechanism_claims", []):
                claim_target = claim.get("target", "").lower()
                if any(term in claim_target for term in search_terms):
                    matches.append({
                        "intervention_id": node.get("intervention_id"),
                        "matched_target": claim.get("target"),
                        "effect": claim.get("effect"),
                        "confidence": claim.get("confidence", "unknown")
                    })
                    break  # Only count each intervention once
        except (json.JSONDecodeError, KeyError):
            continue

    return matches


def search_by_pathway(pathway: str) -> List[Dict]:
    """
    Query Type 3: Find interventions in same signaling pathway.

    Searches primary_pathways and mechanism_claims for pathway terms.
    """
    matches = []
    pathway_lower = pathway.lower()

    # Extract key terms from pathway name
    pathway_terms = re.findall(r'\w+', pathway_lower)

    for intervention_file in INTERVENTIONS_DIR.glob("*.json"):
        try:
            with open(intervention_file, 'r') as f:
                node = json.load(f)

            # Check primary_pathways
            primary_pathways = node.get("primary_pathways", [])
            pathway_match = any(
                any(term in p.lower() for term in pathway_terms)
                for p in primary_pathways
            )

            # Check mechanism_claims
            mechanism_match = any(
                any(term in claim.get("effect", "").lower() for term in pathway_terms)
                for claim in node.get("mechanism_claims", [])
            )

            if pathway_match or mechanism_match:
                matches.append({
                    "intervention_id": node.get("intervention_id"),
                    "primary_pathways": primary_pathways,
                    "match_type": "pathway" if pathway_match else "mechanism"
                })
        except (json.JSONDecodeError, KeyError):
            continue

    return matches


def search_by_indication(indication: str) -> List[Dict]:
    """
    Query Type 4: Find interventions for same clinical indication.

    Searches dosing_protocols[].indication field.
    """
    matches = []
    indication_lower = indication.lower()
    indication_terms = re.findall(r'\w+', indication_lower)

    for intervention_file in INTERVENTIONS_DIR.glob("*.json"):
        try:
            with open(intervention_file, 'r') as f:
                node = json.load(f)

            for protocol in node.get("dosing_protocols", []):
                protocol_indication = protocol.get("indication", "").lower()
                if any(term in protocol_indication for term in indication_terms):
                    matches.append({
                        "intervention_id": node.get("intervention_id"),
                        "matched_indication": protocol.get("indication"),
                        "dose": protocol.get("dose"),
                        "frequency": protocol.get("frequency"),
                        "confidence": protocol.get("confidence", "unknown")
                    })
                    break  # Only count each intervention once
        except (json.JSONDecodeError, KeyError):
            continue

    return matches


def extract_citations(node: Dict) -> List[Dict]:
    """Extract all peer-reviewed citations from a KB node."""
    citations = []
    intervention_id = node.get("intervention_id", "unknown")

    # From dosing_protocols
    for i, protocol in enumerate(node.get("dosing_protocols", [])):
        for cite in protocol.get("peer_reviewed_citations", []):
            citations.append({
                "pmid": cite.get("pmid"),
                "doi": cite.get("doi"),
                "title": cite.get("title"),
                "source": f"{intervention_id}.dosing_protocols[{i}]",
                "confidence": protocol.get("confidence", "low"),
                "context": protocol.get("indication", "")
            })

    # From mechanism_claims
    for i, claim in enumerate(node.get("mechanism_claims", [])):
        for cite in claim.get("peer_reviewed_citations", []):
            citations.append({
                "pmid": cite.get("pmid"),
                "doi": cite.get("doi"),
                "title": cite.get("title"),
                "source": f"{intervention_id}.mechanism_claims[{i}]",
                "confidence": claim.get("confidence", "low"),
                "target": claim.get("target", ""),
                "effect": claim.get("effect", "")
            })

    # Deduplicate by PMID/DOI
    seen = set()
    unique = []
    for cite in citations:
        key = cite.get("pmid") or cite.get("doi") or cite.get("title")
        if key and key not in seen:
            seen.add(key)
            unique.append(cite)

    return unique


def search_by_biomarker(biomarker: str) -> Dict:
    """
    Query Type 5: Find interventions related to a biomarker (for testing products).

    Searches intervention_id, aliases, mechanism_claims, and monitoring fields.
    Returns interventions that affect or are affected by this biomarker.
    """
    biomarker_lower = biomarker.lower()
    matches = []
    all_citations = []

    # Common biomarker aliases
    biomarker_aliases = {
        "butyrate": ["butyrate", "butyric", "scfa", "short-chain fatty acid", "tributyrin"],
        "akkermansia": ["akkermansia", "a. muciniphila"],
        "lactobacillus": ["lactobacillus", "lactiplantibacillus", "l. plantarum"],
        "bifidobacterium": ["bifidobacterium", "b. longum", "bifido"],
        "scfa": ["scfa", "short-chain fatty acid", "butyrate", "propionate", "acetate"],
        "lps": ["lps", "lipopolysaccharide", "endotoxin"],
        "zonulin": ["zonulin", "gut permeability", "leaky gut"],
        "calprotectin": ["calprotectin", "fecal calprotectin"],
    }

    search_terms = [biomarker_lower]
    for key, terms in biomarker_aliases.items():
        if biomarker_lower in terms or key == biomarker_lower:
            search_terms = terms
            break

    for intervention_file in INTERVENTIONS_DIR.glob("*.json"):
        try:
            with open(intervention_file, 'r') as f:
                node = json.load(f)

            relevance_score = 0
            match_reasons = []

            # Check intervention_id
            if any(term in node.get("intervention_id", "").lower() for term in search_terms):
                relevance_score += 3
                match_reasons.append("direct_match")

            # Check aliases
            aliases = [a.lower() for a in node.get("aliases", [])]
            if any(term in alias for term in search_terms for alias in aliases):
                relevance_score += 2
                match_reasons.append("alias_match")

            # Check mechanism_claims
            for claim in node.get("mechanism_claims", []):
                target = claim.get("target", "").lower()
                effect = claim.get("effect", "").lower()
                if any(term in target or term in effect for term in search_terms):
                    relevance_score += 2
                    match_reasons.append("mechanism_match")
                    break

            # Check monitoring
            monitoring = [m.lower() for m in node.get("monitoring", [])]
            if any(term in mon for term in search_terms for mon in monitoring):
                relevance_score += 1
                match_reasons.append("monitoring_match")

            if relevance_score > 0:
                citations = extract_citations(node)
                matches.append({
                    "intervention_id": node.get("intervention_id"),
                    "relevance_score": relevance_score,
                    "match_reasons": match_reasons,
                    "category": node.get("category"),
                    "citation_count": len(citations)
                })
                all_citations.extend(citations)

        except (json.JSONDecodeError, KeyError):
            continue

    # Sort by relevance
    matches.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Deduplicate citations
    seen = set()
    unique_citations = []
    for cite in all_citations:
        key = cite.get("pmid") or cite.get("doi") or cite.get("title")
        if key and key not in seen:
            seen.add(key)
            unique_citations.append(cite)

    return {
        "biomarker": biomarker,
        "search_terms": search_terms,
        "intervention_matches": matches[:20],  # Top 20
        "total_matches": len(matches),
        "citations_extracted": unique_citations,
        "total_citations": len(unique_citations)
    }


def testing_product_report(category: str) -> Dict:
    """
    Generate KB report for a testing/diagnostic product category.

    Maps common test findings to KB interventions and extracts citations.
    """
    # Category-specific biomarker mappings
    category_biomarkers = {
        "microbiome": ["butyrate", "akkermansia", "lactobacillus", "bifidobacterium",
                       "scfa", "fiber", "prebiotic", "probiotic"],
        "sibo": ["hydrogen", "methane", "hydrogen sulfide", "rifaximin", "lactulose",
                 "prokinetic", "antimicrobial"],
        "gut": ["butyrate", "zonulin", "calprotectin", "lps", "gut barrier",
                "inflammation", "permeability"],
        "oral": ["periodontal", "oral microbiome", "streptococcus"],
        "vaginal": ["lactobacillus", "gardnerella", "vaginal microbiome"],
    }

    biomarkers = category_biomarkers.get(category.lower(), ["microbiome", "gut"])

    report = {
        "category": category,
        "biomarkers_queried": biomarkers,
        "interventions_found": [],
        "all_citations": [],
        "actionability_map": []
    }

    seen_interventions = set()
    all_citations = []

    for biomarker in biomarkers:
        result = search_by_biomarker(biomarker)

        for match in result["intervention_matches"]:
            if match["intervention_id"] not in seen_interventions:
                seen_interventions.add(match["intervention_id"])
                report["interventions_found"].append({
                    "intervention_id": match["intervention_id"],
                    "related_biomarker": biomarker,
                    "relevance_score": match["relevance_score"],
                    "category": match["category"]
                })

        all_citations.extend(result["citations_extracted"])

        # Build actionability mapping
        if result["intervention_matches"]:
            top_interventions = [m["intervention_id"] for m in result["intervention_matches"][:3]]
            report["actionability_map"].append({
                "finding": f"Abnormal {biomarker}",
                "kb_interventions": top_interventions,
                "action_context": f"KB contains {len(result['intervention_matches'])} interventions related to {biomarker}"
            })

    # Deduplicate citations
    seen = set()
    for cite in all_citations:
        key = cite.get("pmid") or cite.get("doi") or cite.get("title")
        if key and key not in seen:
            seen.add(key)
            report["all_citations"].append(cite)

    # Filter to high-confidence citations
    report["high_confidence_citations"] = [
        c for c in report["all_citations"]
        if c.get("confidence") in ["high", "moderate"] and (c.get("pmid") or c.get("doi"))
    ]

    return report


def classify_relationship(
    product_node: Optional[Dict],
    related_node: Dict,
    shared_targets: List[str]
) -> str:
    """
    Classify the relationship between two interventions.

    Returns: synergistic, complementary, overlapping, potentially_antagonistic, neutral
    """
    if not product_node:
        return "neutral"

    product_targets = set(
        claim.get("target", "").lower()
        for claim in product_node.get("mechanism_claims", [])
    )
    related_targets = set(
        claim.get("target", "").lower()
        for claim in related_node.get("mechanism_claims", [])
    )

    # Check for overlapping targets
    overlap = product_targets & related_targets

    if len(overlap) > 2:
        return "overlapping"
    elif len(overlap) == 0:
        return "complementary"
    else:
        # Check for potential antagonism
        product_effects = set(
            claim.get("effect", "").lower()
            for claim in product_node.get("mechanism_claims", [])
        )
        related_effects = set(
            claim.get("effect", "").lower()
            for claim in related_node.get("mechanism_claims", [])
        )

        # Simple heuristic: activation vs inhibition of same target
        for target in overlap:
            product_activates = any("activat" in e for e in product_effects)
            related_inhibits = any("inhibit" in e for e in related_effects)
            if product_activates and related_inhibits:
                return "potentially_antagonistic"

        return "synergistic"


def full_report(product_name: str) -> Dict:
    """
    Generate comprehensive KB query report for a product.

    Runs all 4 query types and compiles results.
    """
    report = {
        "product_name": product_name,
        "direct_lookup": None,
        "target_matches": [],
        "pathway_matches": [],
        "indication_matches": [],
        "citations_extracted": [],
        "contraindications": [],
        "monitoring": [],
        "related_interventions": []
    }

    # Query 1: Direct lookup
    lookup_result = direct_lookup(product_name)
    report["direct_lookup"] = {
        "found": lookup_result["found"],
        "slug": lookup_result.get("slug"),
        "node_path": lookup_result.get("node_path")
    }

    product_node = lookup_result.get("node")

    if product_node:
        # Extract from direct match
        report["contraindications"] = product_node.get("contraindications", [])
        report["monitoring"] = product_node.get("monitoring", [])
        report["citations_extracted"] = extract_citations(product_node)

        # Get targets for related queries
        targets = list(set(
            claim.get("target", "").split()[0]  # First word of target
            for claim in product_node.get("mechanism_claims", [])
            if claim.get("target")
        ))[:3]  # Top 3 targets
    else:
        # Infer targets from product name for indirect enrichment
        targets = ["AMPK", "mTOR"]  # Default fallback

    # Query 2: Target matches
    for target in targets:
        matches = search_by_target(target)
        for match in matches:
            if match["intervention_id"] != slugify(product_name):
                match["query_target"] = target
                report["target_matches"].append(match)

    # Query 3: Pathway matches
    pathway_terms = ["nutrient sensing", "autophagy", "inflammation"]
    for pathway in pathway_terms:
        matches = search_by_pathway(pathway)
        for match in matches:
            if match["intervention_id"] != slugify(product_name):
                match["query_pathway"] = pathway
                report["pathway_matches"].append(match)

    # Query 4: Indication matches
    if product_node:
        indications = list(set(
            protocol.get("indication", "").split(",")[0].strip()
            for protocol in product_node.get("dosing_protocols", [])
            if protocol.get("indication")
        ))[:2]
    else:
        indications = ["glycemic", "longevity"]  # Default fallback

    for indication in indications:
        matches = search_by_indication(indication)
        for match in matches:
            if match["intervention_id"] != slugify(product_name):
                match["query_indication"] = indication
                report["indication_matches"].append(match)

    # Compile related interventions with relationship classification
    seen_interventions = set()
    for match in report["target_matches"] + report["pathway_matches"] + report["indication_matches"]:
        intervention_id = match["intervention_id"]
        if intervention_id not in seen_interventions:
            seen_interventions.add(intervention_id)

            related_node = load_intervention(intervention_id)
            if related_node:
                shared = [t for t in targets if any(
                    t.lower() in c.get("target", "").lower()
                    for c in related_node.get("mechanism_claims", [])
                )]

                relationship = classify_relationship(product_node, related_node, shared)

                report["related_interventions"].append({
                    "intervention_id": intervention_id,
                    "relationship": relationship,
                    "shared_targets": shared,
                    "category": related_node.get("category")
                })

    return report


def main():
    parser = argparse.ArgumentParser(description="Query NGM Signaling KB")
    parser.add_argument("--lookup", help="Direct intervention lookup")
    parser.add_argument("--target", help="Search by molecular target")
    parser.add_argument("--pathway", help="Search by signaling pathway")
    parser.add_argument("--indication", help="Search by clinical indication")
    parser.add_argument("--biomarker", help="Search by biomarker (for testing products)")
    parser.add_argument("--testing-report", help="Generate report for testing product category")
    parser.add_argument("--extract-citations", help="Extract all citations from an intervention")
    parser.add_argument("--full-report", help="Generate comprehensive report")
    parser.add_argument("--list", action="store_true", help="List all interventions")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.list:
        interventions = list_all_interventions()
        if args.json:
            print(json.dumps(interventions, indent=2))
        else:
            print(f"Total interventions: {len(interventions)}")
            for i in sorted(interventions):
                print(f"  - {i}")
        return

    if args.lookup:
        result = direct_lookup(args.lookup)
        if args.json:
            # Don't include full node in JSON output
            result_slim = {k: v for k, v in result.items() if k != "node"}
            if result["found"]:
                result_slim["node_summary"] = {
                    "intervention_id": result["node"].get("intervention_id"),
                    "category": result["node"].get("category"),
                    "dosing_protocol_count": len(result["node"].get("dosing_protocols", [])),
                    "mechanism_claim_count": len(result["node"].get("mechanism_claims", [])),
                }
            print(json.dumps(result_slim, indent=2))
        else:
            if result["found"]:
                node = result["node"]
                print(f"FOUND: {result['slug']}")
                print(f"  Category: {node.get('category')}")
                print(f"  Aliases: {node.get('aliases', [])}")
                print(f"  Dosing Protocols: {len(node.get('dosing_protocols', []))}")
                print(f"  Mechanism Claims: {len(node.get('mechanism_claims', []))}")
                print(f"  Contraindications: {len(node.get('contraindications', []))}")
            else:
                print(f"NOT FOUND")
                print(f"  Attempted: {result['attempted_slugs']}")
        return

    if args.target:
        results = search_by_target(args.target)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Target matches for '{args.target}': {len(results)}")
            for r in results[:10]:
                print(f"  - {r['intervention_id']}: {r['matched_target']} ({r['effect']})")
        return

    if args.pathway:
        results = search_by_pathway(args.pathway)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Pathway matches for '{args.pathway}': {len(results)}")
            for r in results[:10]:
                print(f"  - {r['intervention_id']}")
        return

    if args.indication:
        results = search_by_indication(args.indication)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Indication matches for '{args.indication}': {len(results)}")
            for r in results[:10]:
                print(f"  - {r['intervention_id']}: {r['matched_indication']}")
        return

    if args.biomarker:
        result = search_by_biomarker(args.biomarker)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"=== BIOMARKER SEARCH: {args.biomarker} ===\n")
            print(f"Search terms: {result['search_terms']}")
            print(f"Total matches: {result['total_matches']}")
            print(f"Citations extracted: {result['total_citations']}\n")

            print("TOP INTERVENTIONS:")
            for m in result['intervention_matches'][:10]:
                print(f"  - {m['intervention_id']} (score: {m['relevance_score']}, reasons: {m['match_reasons']})")

            print("\nCITATIONS (first 5):")
            for c in result['citations_extracted'][:5]:
                pmid_doi = c.get('pmid') or c.get('doi') or 'no-id'
                conf = c.get('confidence', 'unknown')
                print(f"  - [{conf}] {pmid_doi}: {c.get('title', 'No title')[:60]}...")
        return

    if args.testing_report:
        result = testing_product_report(args.testing_report)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"=== TESTING PRODUCT REPORT: {args.testing_report} ===\n")
            print(f"Biomarkers queried: {result['biomarkers_queried']}")
            print(f"Interventions found: {len(result['interventions_found'])}")
            print(f"Citations extracted: {len(result['all_citations'])}")
            print(f"High-confidence citations: {len(result['high_confidence_citations'])}\n")

            print("ACTIONABILITY MAP:")
            for a in result['actionability_map']:
                print(f"  {a['finding']} → {a['kb_interventions']}")

            print("\nHIGH-CONFIDENCE CITATIONS:")
            for c in result['high_confidence_citations'][:10]:
                pmid_doi = c.get('pmid') or c.get('doi')
                print(f"  - {pmid_doi}: {c.get('title', 'No title')[:50]}...")
        return

    if args.extract_citations:
        lookup_result = direct_lookup(args.extract_citations)
        if lookup_result["found"]:
            citations = extract_citations(lookup_result["node"])
            if args.json:
                print(json.dumps({
                    "intervention_id": args.extract_citations,
                    "total_citations": len(citations),
                    "high_confidence": [c for c in citations if c.get("confidence") in ["high", "moderate"]],
                    "all_citations": citations
                }, indent=2))
            else:
                print(f"=== CITATIONS: {args.extract_citations} ===\n")
                print(f"Total citations: {len(citations)}")
                high_conf = [c for c in citations if c.get("confidence") in ["high", "moderate"]]
                print(f"High/moderate confidence: {len(high_conf)}\n")

                for c in citations:
                    pmid_doi = c.get('pmid') or c.get('doi') or 'no-id'
                    conf = c.get('confidence', 'unknown')
                    print(f"  [{conf}] {pmid_doi}")
                    print(f"    Title: {c.get('title', 'No title')}")
                    if c.get('target'):
                        print(f"    Target: {c.get('target')}")
                    if c.get('effect'):
                        print(f"    Effect: {c.get('effect')[:80]}...")
                    print()
        else:
            print(f"NOT FOUND: {args.extract_citations}")
        return

    if args.full_report:
        report = full_report(args.full_report)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"=== KB QUERY REPORT: {args.full_report} ===\n")
            print(f"DIRECT LOOKUP: {'FOUND' if report['direct_lookup']['found'] else 'NOT FOUND'}")
            if report['direct_lookup']['found']:
                print(f"  Node: {report['direct_lookup']['node_path']}")
            print()

            print(f"TARGET MATCHES: {len(report['target_matches'])}")
            for m in report['target_matches'][:5]:
                print(f"  - {m['intervention_id']} ({m['query_target']})")
            print()

            print(f"PATHWAY MATCHES: {len(report['pathway_matches'])}")
            for m in report['pathway_matches'][:5]:
                print(f"  - {m['intervention_id']} ({m['query_pathway']})")
            print()

            print(f"INDICATION MATCHES: {len(report['indication_matches'])}")
            for m in report['indication_matches'][:5]:
                print(f"  - {m['intervention_id']} ({m['query_indication']})")
            print()

            print(f"CITATIONS EXTRACTED: {len(report['citations_extracted'])}")
            for c in report['citations_extracted'][:5]:
                pmid_doi = c.get('pmid') or c.get('doi') or 'no-id'
                print(f"  - {pmid_doi}: {c.get('title', 'No title')[:50]}...")
            print()

            print(f"RELATED INTERVENTIONS: {len(report['related_interventions'])}")
            for r in report['related_interventions'][:10]:
                print(f"  - {r['intervention_id']} ({r['relationship']})")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
