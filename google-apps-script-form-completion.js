/**
 * Google Apps Script — Form Completion Tracker
 *
 * PURPOSE: When a Google Form is submitted, this script:
 *   1. Finds the matching row in the FormTracking sheet (by form_url)
 *   2. Marks form_completed = true and sets form_completed_at timestamp
 *   3. Sends a confirmation SMS via Twilio ("We received your form — thanks!")
 *
 * SETUP INSTRUCTIONS:
 *
 * Option A — Standalone Script (Recommended):
 *   1. Go to https://script.google.com and create a new project
 *   2. Paste this entire file into Code.gs
 *   3. Fill in the CONFIG section below with your actual values
 *   4. Run setupFormTriggers() once to create triggers for all forms
 *   5. Authorize the script when prompted
 *
 * Option B — Per-Form Script:
 *   1. Open each Google Form in edit mode
 *   2. Click the three-dot menu → Script editor
 *   3. Paste this file
 *   4. In the form's script editor, go to Triggers → Add Trigger
 *   5. Choose onFormSubmit, From form, On form submit
 *
 * IMPORTANT: The FormTracking tab must exist in the spreadsheet with these headers:
 *   call_id | caller_name | caller_phone | insurance_type | form_url |
 *   form_sent_at | reminder_sent | form_completed | reminder_sent_at | form_completed_at
 */

// ============================================================
// CONFIG — Fill in your actual values
// ============================================================
const CONFIG = {
  // Google Sheet with FormTracking tab
  TRACKING_SHEET_ID: '14FqFY4ZyGDeOluYPhbQKNWmZhyPOwi7FFHpnn5c7CG0',
  TRACKING_TAB_NAME: 'FormTracking',

  // Twilio credentials for confirmation SMS
  // Set these via Apps Script: File > Project properties > Script properties
  // Keys: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
  TWILIO_ACCOUNT_SID: PropertiesService.getScriptProperties().getProperty('TWILIO_ACCOUNT_SID'),
  TWILIO_AUTH_TOKEN: PropertiesService.getScriptProperties().getProperty('TWILIO_AUTH_TOKEN'),
  TWILIO_FROM_NUMBER: '+18087451420',

  // n8n webhook for form completion notification
  N8N_WEBHOOK_URL: 'https://n8n.nomanuai.com/webhook/vapi-form-completed',

  // Notification email for Val
  NOTIFY_EMAIL: 'val@equityinsurance.services',

  // Google Form IDs → insurance type mapping
  FORM_ID_MAP: {
    '1nXAAS4HKmuoofX9dqK5vF_llri1zEEThAyOJBI-midk': 'auto',
    '1ye5IHu-M60EVFPcmfYjQ53zoHLFVSuOp9yoVJ-dYmFY': 'commercial_auto',
    '1ZkpKXF_ikkMHCrbYMa7Nw5M8x7STbU6nOXe18kSa0RI': 'homeowners',
    '1a4SelYXb12Ihofm2G4Z8Kmj1vilLvhcFI5QvzufBg_4': 'condo',
    '1UJZb20UgfubgeLkqe3BhmSwQVcDJke_5X8X17p2m_kc': 'renters',
    '1xPRCet_wFHhITOHsa8aEcSc__n5gtXhf18SKuHUBoIM': 'dwelling_fire'
  }
};

// ============================================================
// MAIN HANDLER — Called when any linked form is submitted
// ============================================================
function onFormSubmit(e) {
  try {
    // Get the form that was submitted
    const form = e.source || FormApp.getActiveForm();
    const formId = form.getId();
    const formUrl = form.getPublishedUrl();

    Logger.log('Form submitted: ' + formId + ' (' + formUrl + ')');

    // Open the tracking sheet
    const ss = SpreadsheetApp.openById(CONFIG.TRACKING_SHEET_ID);
    const sheet = ss.getSheetByName(CONFIG.TRACKING_TAB_NAME);

    if (!sheet) {
      Logger.log('ERROR: FormTracking tab not found');
      return;
    }

    // Get all data from the tracking sheet
    const data = sheet.getDataRange().getValues();
    const headers = data[0];

    // Find column indices
    const colFormUrl = headers.indexOf('form_url');
    const colFormCompleted = headers.indexOf('form_completed');
    const colFormCompletedAt = headers.indexOf('form_completed_at');
    const colCallerPhone = headers.indexOf('caller_phone');
    const colCallerName = headers.indexOf('caller_name');
    const colInsuranceType = headers.indexOf('insurance_type');

    if (colFormUrl === -1 || colFormCompleted === -1) {
      Logger.log('ERROR: Required columns not found in FormTracking sheet');
      return;
    }

    // Find matching rows (match by form URL containing the form ID)
    let matchFound = false;

    for (let i = 1; i < data.length; i++) {
      const rowFormUrl = String(data[i][colFormUrl] || '');
      const alreadyCompleted = String(data[i][colFormCompleted] || '');

      // Match if the form URL contains this form's ID and hasn't been completed yet
      if (rowFormUrl.includes(formId) && alreadyCompleted !== 'true') {
        // Mark as completed
        const rowNum = i + 1; // 1-indexed for sheet
        sheet.getRange(rowNum, colFormCompleted + 1).setValue('true');
        sheet.getRange(rowNum, colFormCompletedAt + 1).setValue(new Date().toISOString());

        // Send confirmation SMS
        const callerPhone = String(data[i][colCallerPhone] || '');
        const callerName = String(data[i][colCallerName] || 'there');

        if (callerPhone && callerPhone.length >= 10) {
          sendConfirmationSMS(callerPhone, callerName);
        }

        // Notify n8n webhook
        const insuranceType = String(data[i][colInsuranceType] || CONFIG.FORM_ID_MAP[formId] || 'insurance');
        notifyN8n(callerName, callerPhone, insuranceType, formId);

        // Email Val that form was completed
        notifyVal(callerName, callerPhone, insuranceType);

        matchFound = true;
        Logger.log('Marked row ' + rowNum + ' as completed for phone: ' + callerPhone);

        // Only mark the most recent unfinished match
        break;
      }
    }

    if (!matchFound) {
      Logger.log('No matching unfinished row found for form ID: ' + formId);
    }

  } catch (error) {
    Logger.log('ERROR in onFormSubmit: ' + error.message);
  }
}

// ============================================================
// SEND CONFIRMATION SMS via Twilio
// ============================================================
function sendConfirmationSMS(phone, callerName) {
  try {
    // Ensure E.164 format
    let toNumber = phone.replace(/[\s\-\(\)\+]/g, '');
    if (toNumber.length === 10) {
      toNumber = '+1' + toNumber;
    } else if (toNumber.length === 11 && toNumber.startsWith('1')) {
      toNumber = '+' + toNumber;
    } else if (!toNumber.startsWith('+')) {
      toNumber = '+' + toNumber;
    }

    const smsBody = 'Hi ' + callerName + '! We received your intake form — mahalo! ' +
      'Our team will review it and follow up with your quote soon. ' +
      'Questions? Call us at (808) 593-7746.';

    const url = 'https://api.twilio.com/2010-04-01/Accounts/' +
      CONFIG.TWILIO_ACCOUNT_SID + '/Messages.json';

    const payload = {
      'To': toNumber,
      'From': CONFIG.TWILIO_FROM_NUMBER,
      'Body': smsBody
    };

    const options = {
      'method': 'post',
      'payload': payload,
      'headers': {
        'Authorization': 'Basic ' + Utilities.base64Encode(
          CONFIG.TWILIO_ACCOUNT_SID + ':' + CONFIG.TWILIO_AUTH_TOKEN
        )
      },
      'muteHttpExceptions': true
    };

    const response = UrlFetchApp.fetch(url, options);
    const responseCode = response.getResponseCode();

    if (responseCode === 201) {
      Logger.log('Confirmation SMS sent to ' + toNumber);
    } else {
      Logger.log('SMS send failed (' + responseCode + '): ' + response.getContentText());
    }

  } catch (error) {
    Logger.log('ERROR sending SMS: ' + error.message);
  }
}

// ============================================================
// NOTIFY n8n WEBHOOK — Stops reminder loop
// ============================================================
function notifyN8n(callerName, callerPhone, insuranceType, formId) {
  try {
    const payload = {
      event: 'form_completed',
      caller_name: callerName,
      caller_phone: callerPhone,
      insurance_type: insuranceType,
      form_id: formId,
      completed_at: new Date().toISOString()
    };

    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(CONFIG.N8N_WEBHOOK_URL, options);
    Logger.log('n8n webhook response: ' + response.getResponseCode());
  } catch (error) {
    Logger.log('ERROR notifying n8n: ' + error.message);
  }
}

// ============================================================
// NOTIFY VAL via Email — Form completed alert
// ============================================================
function notifyVal(callerName, callerPhone, insuranceType) {
  try {
    const typeLabels = {
      auto: 'Auto Insurance', commercial_auto: 'Commercial Auto Insurance',
      homeowners: 'Home Insurance', condo: 'Condo Insurance',
      renters: 'Renters Insurance', dwelling_fire: 'Dwelling Fire Insurance'
    };
    const typeLabel = typeLabels[insuranceType] || insuranceType;

    MailApp.sendEmail({
      to: CONFIG.NOTIFY_EMAIL,
      subject: 'Intake Form Completed — ' + callerName + ' (' + typeLabel + ')',
      body: 'Good news! ' + callerName + ' (' + callerPhone + ') has completed their ' +
        typeLabel + ' intake form.\n\n' +
        'Please review the form responses and follow up with their quote.\n\n' +
        '— AI Receptionist System'
    });

    Logger.log('Val notified via email about form completion');
  } catch (error) {
    Logger.log('ERROR notifying Val: ' + error.message);
  }
}

// ============================================================
// SETUP — Run this once to create triggers for all forms
// ============================================================
function setupFormTriggers() {
  // Delete any existing triggers first
  const existingTriggers = ScriptApp.getProjectTriggers();
  for (const trigger of existingTriggers) {
    if (trigger.getHandlerFunction() === 'onFormSubmit') {
      ScriptApp.deleteTrigger(trigger);
    }
  }

  // Create a trigger for each form
  for (const formId of Object.keys(CONFIG.FORM_ID_MAP)) {
    try {
      const form = FormApp.openById(formId);
      ScriptApp.newTrigger('onFormSubmit')
        .forForm(form)
        .onFormSubmit()
        .create();

      Logger.log('Trigger created for: ' + CONFIG.FORM_ID_MAP[formId] +
        ' (' + formId + ')');
    } catch (error) {
      Logger.log('ERROR creating trigger for ' + formId + ': ' + error.message);
    }
  }

  Logger.log('All form triggers created successfully!');
}

// ============================================================
// TEST — Verify connectivity without submitting a form
// ============================================================
function testSetup() {
  // Test 1: Can we access the tracking sheet?
  try {
    const ss = SpreadsheetApp.openById(CONFIG.TRACKING_SHEET_ID);
    const sheet = ss.getSheetByName(CONFIG.TRACKING_TAB_NAME);
    if (sheet) {
      Logger.log('OK: FormTracking sheet found with ' + sheet.getLastRow() + ' rows');
    } else {
      Logger.log('FAIL: FormTracking tab not found. Create it first!');
    }
  } catch (error) {
    Logger.log('FAIL: Cannot access tracking sheet: ' + error.message);
  }

  // Test 2: Can we access the forms?
  for (const formId of Object.keys(CONFIG.FORM_ID_MAP)) {
    try {
      const form = FormApp.openById(formId);
      Logger.log('OK: Form "' + form.getTitle() + '" accessible');
    } catch (error) {
      Logger.log('FAIL: Cannot access form ' + formId + ': ' + error.message);
    }
  }

  Logger.log('Setup test complete!');
}
