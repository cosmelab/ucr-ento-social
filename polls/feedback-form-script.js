// GOOGLE APPS SCRIPT FOR FEEDBACK FORM
// Instructions:
// 1. Open your Feedback Form Google Sheet: https://docs.google.com/spreadsheets/d/1pGTToki6Cpd01hq9N3k0dvvFsjDUSqIiZwCEcYH9v2o/edit
// 2. Go to Extensions > Apps Script
// 3. Delete any existing code
// 4. Copy ALL the code from this file and paste it there
// 5. Click Deploy > New deployment > Web app
// 6. Execute as: Me, Who has access: Anyone
// 7. Click Deploy and copy the Web app URL

function doPost(e) {
  try {
    var data = e.parameter;

    // VALIDATE UCR EMAIL (if provided - email is optional for feedback)
    var email = data.email || '';
    if (email && !email.endsWith('@ucr.edu')) {
      return ContentService.createTextOutput(JSON.stringify({
        result: 'error',
        error: 'If providing an email, please use your UCR email address (@ucr.edu)'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    var rowData = [
      new Date(),
      data.name || '',
      data.email || '',
      data.role || '',
      data.feedback_type || '',
      data.suggestions || ''
    ];

    sheet.appendRow(rowData);

    // Send email notification
    var emailAddress = 'lcosme@ucr.edu';
    var subject = 'New Feedback Submission - UCR Ento Social Committee';
    var message = 'New feedback submission:\n\n' +
                  'Name: ' + (data.name || 'Anonymous') + '\n' +
                  'Email: ' + (data.email || 'Not provided') + '\n' +
                  'Role: ' + (data.role || 'Not specified') + '\n' +
                  'Feedback Type: ' + (data.feedback_type || 'Not specified') + '\n' +
                  'Message: ' + (data.suggestions || 'Not provided') + '\n\n' +
                  'View all submissions: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl();

    MailApp.sendEmail(emailAddress, subject, message);

    return ContentService.createTextOutput(JSON.stringify({result: 'success'}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({result: 'error', error: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
