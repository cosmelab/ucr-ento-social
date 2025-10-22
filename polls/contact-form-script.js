// GOOGLE APPS SCRIPT FOR CONTACT FORM
// Instructions:
// 1. Open your Contact Form Google Sheet: https://docs.google.com/spreadsheets/d/1w6ttBktXG5Jdd5i8Guc8GhrRjzlkHPg65nz74EwNQJw/edit
// 2. Go to Extensions > Apps Script
// 3. Delete any existing code
// 4. Copy ALL the code from this file and paste it there
// 5. Click Deploy > New deployment > Web app
// 6. Execute as: Me, Who has access: Anyone
// 7. Click Deploy and copy the Web app URL

function doPost(e) {
  try {
    var data = e.parameter;

    // VALIDATE UCR EMAIL
    var email = data.email || '';
    if (!email.endsWith('@ucr.edu')) {
      return ContentService.createTextOutput(JSON.stringify({
        result: 'error',
        error: 'Please use your UCR email address (@ucr.edu)'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    var rowData = [
      new Date(),
      data.name || '',
      data.email || '',
      data.subject || '',
      data.message || ''
    ];

    sheet.appendRow(rowData);

    // Send email notification
    var emailAddress = 'lcosme@ucr.edu';
    var subject = 'New Contact Form Submission - UCR Ento Social Committee';
    var message = 'New contact form submission:\n\n' +
                  'Name: ' + (data.name || 'Not provided') + '\n' +
                  'Email: ' + (data.email || 'Not provided') + '\n' +
                  'Subject: ' + (data.subject || 'Not provided') + '\n' +
                  'Message: ' + (data.message || 'Not provided') + '\n\n' +
                  'View all submissions: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl();

    MailApp.sendEmail(emailAddress, subject, message);

    return ContentService.createTextOutput(JSON.stringify({result: 'success'}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({result: 'error', error: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
