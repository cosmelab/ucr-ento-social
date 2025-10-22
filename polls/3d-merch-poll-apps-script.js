/**
 * UCR Entomology Social Committee - 3D Print Merchandise Poll
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
 * 6. Copy the Web App URL and update poll-3d-merch.html form action
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
      formData.purchaseInterest || '',
      formData.keychainProducts || '',
      formData.decorativeProducts || '',
      formData.functionalProducts || '',
      formData.favoriteInsects || '',
      formData.designStyle || '',
      formData.printingMethod || '',
      formData.colorPreference || '',
      formData.sizePreference || '',  // New field
      formData.priceSmall || '',
      formData.priceLarge || '',
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
    .createTextOutput('3D Merch Poll Form Handler is active')
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Send notification to admin about new response
 */
function sendAdminNotification(formData) {
  const subject = 'New 3D Print Merchandise Poll Response';

  const body = `
New response received for 3D Print Merchandise Poll

Timestamp: ${new Date().toISOString()}
Email: ${formData.email || 'N/A'}

INTEREST:
- Purchase Interest: ${formData.purchaseInterest || 'N/A'}

PRODUCTS:
- Keychains: ${formData.keychainProducts || 'N/A'}
- Decorative: ${formData.decorativeProducts || 'N/A'}
- Functional: ${formData.functionalProducts || 'N/A'}
- Favorite Insects: ${formData.favoriteInsects || 'N/A'}

DESIGN & PRINTING:
- Style: ${formData.designStyle || 'N/A'}
- Printing Method: ${formData.printingMethod || 'N/A'}
- Colors: ${formData.colorPreference || 'N/A'}
- Size: ${formData.sizePreference || 'N/A'}

PRICING:
- Small Items: ${formData.priceSmall || 'N/A'}
- Large Items: ${formData.priceLarge || 'N/A'}

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
    'Purchase Interest',
    'Keychain Products',
    'Decorative Products',
    'Functional Products',
    'Favorite Insects',
    'Design Style',
    'Printing Method',
    'Color Preference',
    'Size Preference',
    'Price Small Items',
    'Price Large Items',
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

  // Purchase Interest (column 2)
  const interest = countItems(2);
  summary.purchaseInterest = Object.entries(interest)
    .sort((a, b) => b[1] - a[1]);

  // Favorite Insects (column 6)
  const insects = countItems(6);
  summary.favoriteInsects = Object.entries(insects)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  // Design Style (column 7)
  const styles = countItems(7);
  summary.designStyle = Object.entries(styles)
    .sort((a, b) => b[1] - a[1]);

  // Log summary
  Logger.log('=== 3D Merch Poll Summary ===');
  Logger.log(`Total Responses: ${totalResponses}`);
  Logger.log(`Last Response: ${summary.lastResponseTime}`);
  Logger.log('\nPurchase Interest:');
  summary.purchaseInterest.forEach(([interest, count]) => {
    Logger.log(`  ${interest}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });
  Logger.log('\nTop 5 Favorite Insects:');
  summary.favoriteInsects.forEach(([insect, count]) => {
    Logger.log(`  ${insect}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
  });
  Logger.log('\nDesign Style Preferences:');
  summary.designStyle.forEach(([style, count]) => {
    Logger.log(`  ${style}: ${count} (${(count/totalResponses*100).toFixed(1)}%)`);
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
  summarySheet.getRange(row, 1).setValue('3D Print Merchandise Poll - Summary Report');
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
  analyzeColumn(2, 'Purchase Interest Level');
  analyzeColumn(3, 'Keychain Products');
  analyzeColumn(4, 'Decorative Products');
  analyzeColumn(5, 'Functional Products');
  analyzeColumn(6, 'Favorite Insects (Top Priority!)');
  analyzeColumn(7, 'Design Style Preferences');
  analyzeColumn(8, 'Printing Method Preferences');
  analyzeColumn(9, 'Color Preferences');
  analyzeColumn(10, 'Size Preferences');
  analyzeColumn(11, 'Price Range - Small Items');
  analyzeColumn(12, 'Price Range - Large Items');

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
