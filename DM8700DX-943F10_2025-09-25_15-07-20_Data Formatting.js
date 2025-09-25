/*******************************************************************************
 * COGNEX Dataman Script data formating.
 * This script parses a fixed-width data format for different product models.
 *
 * - Model A Format: "A<batch[8]><MFG[6]><EXP[6]><serial[variable]>"
 *   - Example: "A12345678250925310925SN1001"
 *
 *
 ******************************************************************************/

function onResult(decodeResults, readerProperties, output) {
  if (decodeResults.length > 0 && decodeResults[0].decoded) {
    var rawContent = decodeResults[0].content;
    var formattedContent = "";

    // --- Model-Based Logic ---

    // Check for Model A: Fixed-position format
    if (rawContent.startsWith("A")) {
      try {
        // Use substring to extract data based on character position.
        // substring(startIndex, endIndex) - endIndex is not included.
        var batch = rawContent.substring(2, 9); // Characters 1 through 7
        var mfgDateRaw = rawContent.substring(9, 15); // Characters 8 through 13
        var expDateRaw = rawContent.substring(15, 21); // Characters 14 through 19
        var serialNumber = rawContent.substring(21); // From character 20 to the end

        // Format the dates from DDMMYY to a more readable format.
        var mfgDateFormatted = "20" + mfgDateRaw.substring(4, 6) + "-" + mfgDateRaw.substring(2, 4) + "-" + mfgDateRaw.substring(0, 2);
        var expDateFormatted = "20" + expDateRaw.substring(4, 6) + "-" + expDateRaw.substring(2, 4) + "-" + expDateRaw.substring(0, 2);

        // Construct the final, readable output string.
        formattedContent = "\n\rModel: A, Batch: " + batch + 
					", \n\rMFG: "+ mfgDateFormatted + 
					", \n\rEXP: " + expDateFormatted + 
					", \n\rS/N: " + serialNumber + 
					"\n\r";
      } catch (e) {
        formattedContent = "Error: Invalid Model A format - " + rawContent;
      }
    }
    // Check for Model B (example from before)
    else if (rawContent.startsWith("B-")) {
      var parts = rawContent.split('-');
      if (parts.length === 2) {
        formattedContent = "Serial: " + parts[1];
      } else {
        formattedContent = "Error: Invalid Model B format";
      }
    }
    // --- Fallback for Unrecognized Models ---
    else {
      formattedContent = "Unrecognized Model: " + rawContent;
    }

    // Set the final string that the reader will output.
    output.content = formattedContent;

  } else {
    // If no code was read, send a "NOREAD" message.
    output.content = "NOREAD";
  }
}
