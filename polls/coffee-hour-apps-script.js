/**
 * UCR Entomology Social Committee - Coffee Hour Poll
 * Google Apps Script for form handling
 *
 * Setup Instructions:
 * 1. Create a new Google Spreadsheet for responses
 * 2. Go to Extensions > Apps Script
 * 3. Replace default code with this script
 * 4. Run setupHeaders() function once to initialize the sheet
 * 5. Deploy as Web App:
 *    - Click Deploy > New deployment
 *    - Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone at UC Riverside (ucr.edu)
 * 6. Copy the Web App URL and update poll-coffee-hour.html form action
 */

// Configuration
const ADMIN_EMAIL = 'lcosme@ucr.edu';
const SEND_ADMIN_NOTIFICATION = false; // Set to true to receive email notifications

/**
 * Handle POST requests from the web form
 */
function doPost(e) {
  try {
    // Get form data
    const formData = e.parameter;

    // VALIDATE UCR EMAIL
    const email = formData.email || '';
    if (!email.endsWith('@ucr.edu')) {
      return ContentService
        .createTextOutput(JSON.stringify({
          'result': 'error',
          'error': 'Please use your UCR email address (@ucr.edu)'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Get the active spreadsheet
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Create array for the row data matching the header order
    const rowData = [
      new Date().toISOString(), // Timestamp
      formData.email || '',
      formData.role || '',
      formData.frequency || '',
      formData.days || '',
      formData.duration || '',
      formData.startTime || '',
      formData.coffeeTypes || '',
      formData.teaTypes || '',
      formData.foodOptions || '',
      formData.environment || '',
      formData.location || '',
      formData.labHosting || '',
      formData.musicTypes || '',
      formData.barriers || '',
      formData.suggestions || ''
    ];

    // Append the data to the sheet
    sheet.appendRow(rowData);

    // Send admin notification if enabled
    if (SEND_ADMIN_NOTIFICATION) {
      sendAdminNotification(formData);
    }

    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        'result': 'success',
        'row': sheet.getLastRow()
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Log error for debugging
    console.error('Error in doPost:', error);

    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        'result': 'error',
        'error': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function to verify the script is working
function doGet(e) {
  return ContentService
    .createTextOutput('Coffee Hour Poll Form Handler is active')
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Send notification to admin about new response
 */
function sendAdminNotification(formData) {
  const subject = 'New Coffee Hour Poll Response';

  const body = `
New response received for Coffee Hour Poll

Timestamp: ${new Date().toISOString()}
Email: ${formData.email || 'N/A'}

ABOUT YOU:
- Role: ${formData.role || 'N/A'}

SCHEDULING:
- Frequency: ${formData.frequency || 'N/A'}
- Preferred Days: ${formData.days || 'N/A'}
- Duration: ${formData.duration || 'N/A'}
- Start Time: ${formData.startTime || 'N/A'}

FOOD & BEVERAGES:
- Coffee Types: ${formData.coffeeTypes || 'N/A'}
- Tea Types: ${formData.teaTypes || 'N/A'}
- Food Options: ${formData.foodOptions || 'N/A'}

LOCATION & ENVIRONMENT:
- Environment: ${formData.environment || 'N/A'}
- Location: ${formData.location || 'N/A'}
- Music Types: ${formData.musicTypes || 'N/A'}

PARTICIPATION:
- Lab Hosting: ${formData.labHosting || 'N/A'}
- Barriers: ${formData.barriers || 'N/A'}

SUGGESTIONS:
${formData.suggestions || 'None'}

View all responses in your spreadsheet.
  `;

  try {
    GmailApp.sendEmail(ADMIN_EMAIL, subject, body);
  } catch (error) {
    console.error('Error sending admin notification:', error);
  }
}

/**
 * Set up headers (run once after creating the spreadsheet)
 */
function setupHeaders() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const headers = [
    'Timestamp',
    'Email',
    'Role',
    'Frequency',
    'Preferred Days',
    'Duration',
    'Start Time',
    'Coffee Types',
    'Tea Types',
    'Food Options',
    'Environment Preference',
    'Location Preference',
    'Lab Hosting Willingness',
    'Music Types',
    'Barriers',
    'Additional Suggestions'
  ];

  // Clear existing content and set headers
  sheet.clear();
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format header row
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight('bold');
  headerRange.setBackground('#4A90E2');
  headerRange.setFontColor('#FFFFFF');

  // Set column widths for better readability
  sheet.setColumnWidth(1, 150); // Timestamp
  for (let i = 2; i <= headers.length; i++) {
    sheet.setColumnWidth(i, 220);
  }

  // Freeze the header row
  sheet.setFrozenRows(1);

  Logger.log('Headers set up successfully!');
}

/**
 * Get summary statistics (run manually to view stats)
 */
function getSummaryStats() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();

  if (data.length <= 1) {
    Logger.log('No responses yet');
    return 'No responses yet';
  }

  const totalResponses = data.length - 1;
  const summary = {
    totalResponses: totalResponses,
    lastResponseTime: data[data.length - 1][0]
  };

  // Helper function to count items
  function countItems(columnIndex) {
    const counts = {};
    for (let i = 1; i < data.length; i++) {
      const items = (data[i][columnIndex] || '').split(', ');
      items.forEach(item => {
        if (item.trim()) {
          counts[item] = (counts[item] || 0) + 1;
        }
      });
    }
    return counts;
  }

  // Role distribution (column 2)
  const roles = countItems(2);
  summary.roles = Object.entries(roles)
    .sort((a, b) => b[1] - a[1]);

  // Preferred Days (column 4)
  const days = countItems(4);
  summary.days = Object.entries(days)
    .sort((a, b) => b[1] - a[1]);

  // Start Time (column 6)
  const startTimes = countItems(6);
  summary.startTimes = Object.entries(startTimes)
    .sort((a, b) => b[1] - a[1]);

  // Log summary
  Logger.log('=== Coffee Hour Poll Summary ===');
  Logger.log(`Total Responses: ${totalResponses}`);
  Logger.log(`Last Response: ${summary.lastResponseTime}`);
  Logger.log('\nRole Distribution:');
  summary.roles.forEach(([role, count]) => {
    Logger.log(`  ${role}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });
  Logger.log('\nPreferred Days:');
  summary.days.forEach(([day, count]) => {
    Logger.log(`  ${day}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });
  Logger.log('\nStart Times:');
  summary.startTimes.forEach(([time, count]) => {
    Logger.log(`  ${time}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });

  return summary;
}

/**
 * Create a formatted summary report in a new sheet
 */
function createSummaryReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const dataSheet = ss.getActiveSheet();
  const data = dataSheet.getDataRange().getValues();

  if (data.length <= 1) {
    Logger.log('No responses yet to create a report');
    return;
  }

  // Create or get summary sheet
  let summarySheet = ss.getSheetByName('Summary');
  if (summarySheet) {
    summarySheet.clear();
  } else {
    summarySheet = ss.insertSheet('Summary');
  }

  const totalResponses = data.length - 1;
  let row = 1;

  // Title
  summarySheet.getRange(row, 1).setValue('Coffee Hour Poll - Summary Report');
  summarySheet.getRange(row, 1).setFontWeight('bold').setFontSize(16);
  row += 2;

  // Metadata
  summarySheet.getRange(row, 1).setValue(`Generated: ${new Date()}`);
  row++;
  summarySheet.getRange(row, 1).setValue(`Total Responses: ${totalResponses}`);
  row += 2;

  // Helper function to count and display results
  function analyzeColumn(columnIndex, title) {
    const counts = {};
    for (let i = 1; i < data.length; i++) {
      const items = (data[i][columnIndex] || '').split(', ');
      items.forEach(item => {
        if (item.trim()) {
          counts[item] = (counts[item] || 0) + 1;
        }
      });
    }

    if (Object.keys(counts).length === 0) return;

    summarySheet.getRange(row, 1).setValue(title);
    summarySheet.getRange(row, 1).setFontWeight('bold').setBackground('#E8F4F8');
    row++;

    Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .forEach(([item, count]) => {
        summarySheet.getRange(row, 1).setValue(item);
        summarySheet.getRange(row, 2).setValue(count);
        summarySheet.getRange(row, 3).setValue(`${(count/totalResponses*100).toFixed(1)}%`);
        row++;
      });
    row++;
  }

  // Analyze key columns
  analyzeColumn(2, 'Role Distribution');
  analyzeColumn(3, 'Frequency Preferences');
  analyzeColumn(4, 'Preferred Days (MOST IMPORTANT!)');
  analyzeColumn(5, 'Duration');
  analyzeColumn(6, 'Start Times (MOST IMPORTANT!)');
  analyzeColumn(7, 'Coffee Types');
  analyzeColumn(8, 'Tea Types');
  analyzeColumn(9, 'Food Options');
  analyzeColumn(10, 'Environment Preference');
  analyzeColumn(11, 'Location Preference');
  analyzeColumn(12, 'Lab Hosting Willingness');
  analyzeColumn(13, 'Music Types');
  analyzeColumn(14, 'Barriers to Attendance');

  // Format the summary sheet
  summarySheet.setColumnWidth(1, 400);
  summarySheet.setColumnWidth(2, 100);
  summarySheet.setColumnWidth(3, 100);

  // Add column headers
  summarySheet.getRange(5, 2).setValue('Count');
  summarySheet.getRange(5, 3).setValue('Percentage');
  summarySheet.getRange(5, 2, 1, 2).setFontWeight('bold');

  Logger.log('Summary report created successfully!');
}
