/**
 * UCR Entomology Social Committee - Events & Activities Poll (Redesigned)
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
 * 6. Copy the Web App URL and update poll-events-new.html form action
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
      formData.onCampusSocial || '',
      formData.onCampusGames || '',
      formData.seasonalEvents || '',
      formData.outdoorActivities || '',
      formData.dayTrips || '',
      formData.entertainment || '',
      formData.eventFrequency || '',
      formData.availability || '',
      formData.barriers || '',
      formData.eventBudget || '',
      formData['3dprintInterest'] || '',
      formData.participation || '',
      formData.alcoholPreference || '',
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
    .createTextOutput('Events Poll Form Handler is active')
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Send notification to admin about new response
 */
function sendAdminNotification(formData) {
  const subject = 'New Events & Activities Poll Response';

  const body = `
New response received for Events & Activities Poll (Redesigned)

Timestamp: ${new Date().toISOString()}
Email: ${formData.email || 'N/A'}

ON-CAMPUS EVENTS:
- Social Events: ${formData.onCampusSocial || 'N/A'}
- Games & Entertainment: ${formData.onCampusGames || 'N/A'}
- Seasonal Celebrations: ${formData.seasonalEvents || 'N/A'}

OFF-CAMPUS ACTIVITIES:
- Outdoor Activities: ${formData.outdoorActivities || 'N/A'}
- Day Trips: ${formData.dayTrips || 'N/A'}
- Entertainment: ${formData.entertainment || 'N/A'}

TIMING & LOGISTICS:
- Event Frequency: ${formData.eventFrequency || 'N/A'}
- Availability: ${formData.availability || 'N/A'}
- Main Barriers: ${formData.barriers || 'N/A'}

FUNDRAISING:
- Event Budget: ${formData.eventBudget || 'N/A'}
- 3D Print Interest: ${formData['3dprintInterest'] || 'N/A'}

PARTICIPATION:
- How to Help: ${formData.participation || 'N/A'}
- Alcohol Preference: ${formData.alcoholPreference || 'N/A'}

ADDITIONAL SUGGESTIONS:
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
    'On-Campus Social Events',
    'On-Campus Games & Entertainment',
    'Seasonal Celebrations',
    'Outdoor Activities',
    'Day Trips',
    'Entertainment Outings',
    'Event Frequency',
    'Availability Times',
    'Main Barriers',
    'Event Budget',
    '3D Print Interest',
    'Participation Level',
    'Alcohol Preference',
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
    sheet.setColumnWidth(i, 250);
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

  // Event Frequency (column 8)
  const frequency = countItems(8);
  summary.eventFrequency = Object.entries(frequency)
    .sort((a, b) => b[1] - a[1]);

  // Fundraising Ideas (column 12)
  const fundraising = countItems(12);
  summary.fundraisingIdeas = Object.entries(fundraising)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  // Event Budget (column 11)
  const budget = countItems(11);
  summary.eventBudget = Object.entries(budget)
    .sort((a, b) => b[1] - a[1]);

  // Log summary
  Logger.log('=== Events Poll Summary ===');
  Logger.log(`Total Responses: ${totalResponses}`);
  Logger.log(`Last Response: ${summary.lastResponseTime}`);
  Logger.log('\nEvent Frequency Preferences:');
  summary.eventFrequency.forEach(([freq, count]) => {
    Logger.log(`  ${freq}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });
  Logger.log('\nTop Fundraising Ideas (including 3D print merch):');
  summary.fundraisingIdeas.forEach(([idea, count]) => {
    Logger.log(`  ${idea}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });
  Logger.log('\nBudget Preferences:');
  summary.eventBudget.forEach(([budget, count]) => {
    Logger.log(`  ${budget}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
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
  summarySheet.getRange(row, 1).setValue('Events & Activities Poll - Summary Report');
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
  analyzeColumn(2, 'ON-CAMPUS: Social Events');
  analyzeColumn(3, 'ON-CAMPUS: Games & Entertainment');
  analyzeColumn(4, 'Seasonal Celebrations');
  analyzeColumn(5, 'OFF-CAMPUS: Outdoor Activities');
  analyzeColumn(6, 'OFF-CAMPUS: Day Trips');
  analyzeColumn(7, 'Entertainment Outings');

  row++;
  summarySheet.getRange(row, 1).setValue('KEY LOGISTICS');
  summarySheet.getRange(row, 1).setFontWeight('bold').setFontSize(14).setBackground('#D1E7F5');
  row += 2;

  analyzeColumn(8, 'Event Frequency Preferences');
  analyzeColumn(9, 'Best Availability Times');
  analyzeColumn(10, 'Main Barriers to Attendance');

  row++;
  summarySheet.getRange(row, 1).setValue('FUNDRAISING & BUDGET');
  summarySheet.getRange(row, 1).setFontWeight('bold').setFontSize(14).setBackground('#D1E7F5');
  row += 2;

  analyzeColumn(11, 'Event Budget Willingness');
  analyzeColumn(12, 'Fundraising Ideas (including 3D print merch)');

  row++;
  summarySheet.getRange(row, 1).setValue('PARTICIPATION');
  summarySheet.getRange(row, 1).setFontWeight('bold').setFontSize(14).setBackground('#D1E7F5');
  row += 2;

  analyzeColumn(13, 'How People Want to Participate');
  analyzeColumn(14, 'Alcohol Preferences');

  // Format the summary sheet
  summarySheet.setColumnWidth(1, 450);
  summarySheet.setColumnWidth(2, 100);
  summarySheet.setColumnWidth(3, 100);

  // Add column headers
  summarySheet.getRange(5, 2).setValue('Count');
  summarySheet.getRange(5, 3).setValue('Percentage');
  summarySheet.getRange(5, 2, 1, 2).setFontWeight('bold');

  Logger.log('Summary report created successfully!');
}

/**
 * Export data-friendly version for analysis (CSV-like format)
 */
function createDataAnalysisSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const dataSheet = ss.getActiveSheet();
  const data = dataSheet.getDataRange().getValues();

  if (data.length <= 1) {
    Logger.log('No responses yet');
    return;
  }

  // Create or get analysis sheet
  let analysisSheet = ss.getSheetByName('Data Analysis');
  if (analysisSheet) {
    analysisSheet.clear();
  } else {
    analysisSheet = ss.insertSheet('Data Analysis');
  }

  // This creates a binary (yes/no) matrix for each option
  // Useful for statistical analysis and visualization

  const headers = data[0];
  const responses = data.slice(1);

  // Columns to expand (checkbox groups)
  const expandColumns = [2, 3, 4, 5, 6, 7, 9, 10, 12, 13]; // All multi-select columns

  // Create new header row
  const newHeaders = ['Timestamp'];
  const allOptions = {};

  // First pass: collect all unique options
  expandColumns.forEach(colIdx => {
    allOptions[colIdx] = new Set();
    responses.forEach(row => {
      const items = (row[colIdx] || '').split(', ');
      items.forEach(item => {
        if (item.trim()) allOptions[colIdx].add(item.trim());
      });
    });
  });

  // Build header row
  expandColumns.forEach(colIdx => {
    const categoryName = headers[colIdx];
    allOptions[colIdx].forEach(option => {
      newHeaders.push(`${categoryName}: ${option}`);
    });
  });

  // Add single-choice columns
  newHeaders.push('Event Frequency');
  newHeaders.push('Event Budget');
  newHeaders.push('Alcohol Preference');

  analysisSheet.getRange(1, 1, 1, newHeaders.length).setValues([newHeaders]);
  analysisSheet.getRange(1, 1, 1, newHeaders.length).setFontWeight('bold');

  // Fill in data
  responses.forEach((row, rowIdx) => {
    const newRow = [row[0]]; // Timestamp

    // Expand multi-select columns
    expandColumns.forEach(colIdx => {
      const selectedItems = (row[colIdx] || '').split(', ').map(s => s.trim());
      allOptions[colIdx].forEach(option => {
        newRow.push(selectedItems.includes(option) ? '1' : '0');
      });
    });

    // Add single-choice columns
    newRow.push(row[8] || ''); // Event Frequency
    newRow.push(row[11] || ''); // Event Budget
    newRow.push(row[14] || ''); // Alcohol Preference

    analysisSheet.getRange(rowIdx + 2, 1, 1, newRow.length).setValues([newRow]);
  });

  analysisSheet.setFrozenRows(1);
  analysisSheet.setFrozenColumns(1);

  Logger.log('Data analysis sheet created! Use this for statistical analysis.');
}
