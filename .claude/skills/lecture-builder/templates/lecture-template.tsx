
import React from 'react';
import { Link } from 'wouter';
import MentorshipAccessGate from '@/components/MentorshipAccessGate';
import {
  ArrowLeft,
  Clock,
  BookOpen,
  // Add additional icons as needed
} from 'lucide-react';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';

const LectureTitleHere: React.FC = () => {
  return (
    <MentorshipAccessGate>
      <div className="min-h-screen bg-white">
        <Navbar />

        {/* Navigation Breadcrumb */}
        <nav className="border-b border-gray-100 bg-white">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <div className="flex items-center gap-4">
              <Link href="/mentorship-content" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors">
                <ArrowLeft className="w-4 h-4" />
                <span className="text-sm">Back to Curriculum</span>
              </Link>
              <div className="text-gray-300">/</div>
              <span className="text-sm text-gray-900 font-medium">TRACK_NAME</span>
            </div>
          </div>
        </nav>

        {/* Header Section */}
        <header className="bg-gradient-to-br from-indigo-50 via-purple-50 to-blue-50 border-b border-indigo-100/50">
          <div className="max-w-4xl mx-auto px-6 py-12">
            <div className="flex items-center gap-3 text-xs uppercase tracking-wider text-indigo-600 mb-6">
              <span className="bg-indigo-100 px-3 py-1 rounded-full font-medium">TRACK_NAME</span>
              <span>•</span>
              <span>SUBTRACK_NAME</span>
            </div>

            <h1 className="text-3xl font-light text-gray-900 mb-6 tracking-tight leading-tight">
              LECTURE_TITLE
            </h1>

            <p className="text-lg text-gray-600 leading-relaxed mb-8 max-w-3xl">
              LECTURE_ABSTRACT
            </p>

            <div className="flex flex-wrap items-center gap-6 text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>DURATION</span>
              </div>
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                <span>TAG_1</span>
              </div>
              {/* Add more tags as needed */}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-6 py-12">
          <div className="prose prose-lg max-w-none">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Video Lecture</h2>

            {/* Descript Video Embed */}
            <div className="my-8 flex justify-center">
              <div className="w-full max-w-3xl">
                <div className="relative bg-gray-100 rounded-lg overflow-hidden shadow-lg" style={{ paddingBottom: '56.25%' }}>
                  <iframe
                    src="DESCRIPT_IFRAME_URL"
                    className="absolute top-0 left-0 w-full h-full"
                    frameBorder="0"
                    allowFullScreen
                   allow="autoplay; fullscreen"></iframe>
                </div>
              </div>
            </div>

            {/* HTML Content from provided file */}
            <div className="mt-12">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6 border-b-2 border-blue-500 pb-3">The Fundamental Shift</h2>

              <p className="mb-6">CONTENT_PARAGRAPH_1</p>

              <p className="mb-6">CONTENT_PARAGRAPH_2</p>

              <h2 className="text-2xl font-semibold text-gray-900 mb-6 mt-12 border-b-2 border-blue-500 pb-3">How CORE_CONCEPT Works</h2>

              <p className="mb-6">MECHANISM_CONTENT</p>

              <h2 className="text-2xl font-semibold text-gray-900 mb-6 mt-12 border-b-2 border-blue-500 pb-3">Clinical Performance Evidence</h2>

              <p className="mb-6">EVIDENCE_CONTENT</p>

              <h2 className="text-2xl font-semibold text-gray-900 mb-6 mt-12 border-b-2 border-blue-500 pb-3">DOMAIN Applications</h2>

              <p className="mb-6">APPLICATION_CONTENT</p>

              {/* Additional sections as needed (5-7 total content sections) */}

              <h2 className="text-2xl font-semibold text-gray-900 mb-6 mt-12 border-b-2 border-blue-500 pb-3">Key Mechanisms and Clinical Takeaways</h2>

              <div className="overflow-x-auto my-8">
                <table className="min-w-full border-collapse">
                  <thead>
                    <tr className="bg-blue-600 text-white">
                      <th className="border border-gray-300 px-4 py-3 text-left">Core Mechanism</th>
                      <th className="border border-gray-300 px-4 py-3 text-left">Clinical Application</th>
                      <th className="border border-gray-300 px-4 py-3 text-left">Implementation Consideration</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="even:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-3">MECHANISM_1</td>
                      <td className="border border-gray-300 px-4 py-3">APPLICATION_1</td>
                      <td className="border border-gray-300 px-4 py-3">CONSIDERATION_1</td>
                    </tr>
                    <tr className="even:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-3">MECHANISM_2</td>
                      <td className="border border-gray-300 px-4 py-3">APPLICATION_2</td>
                      <td className="border border-gray-300 px-4 py-3">CONSIDERATION_2</td>
                    </tr>
                    {/* Add more rows as needed */}
                  </tbody>
                </table>
              </div>

              <h2 className="text-2xl font-semibold text-gray-900 mb-6 mt-12 border-b-2 border-blue-500 pb-3">Implementation Pathway</h2>

              <p className="mb-6"><strong>Start with...</strong> IMPLEMENTATION_STEP_1</p>

              <p className="mb-6"><strong>Build...</strong> IMPLEMENTATION_STEP_2</p>

              <p className="mb-6"><strong>Integrate...</strong> IMPLEMENTATION_STEP_3</p>

              <h2 className="text-2xl font-semibold text-gray-900 mb-6 mt-12 border-b-2 border-blue-500 pb-3">The Path Forward</h2>

              <p className="mb-6">PATH_FORWARD_PARAGRAPH_1</p>

              <p className="mb-6">PATH_FORWARD_PARAGRAPH_2</p>

              <div className="mt-12 pt-8 border-t border-gray-200">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">References</h3>
                <div className="text-sm text-gray-700 space-y-2">
                  <p>[1] REFERENCE_1</p>
                  <p>[2] REFERENCE_2</p>
                  <p>[3] REFERENCE_3</p>
                  {/* Add more references as needed */}
                </div>
              </div>
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </MentorshipAccessGate>
  );
};

export default LectureTitleHere;
