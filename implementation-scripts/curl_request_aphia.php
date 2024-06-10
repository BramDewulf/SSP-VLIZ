<?php 
    $citation = "Hobbs III, H H. (1978). New species of ostracods from the Gulf Coastal Plain (Ostracoda: Entocytheridae). Transactions of the American Microscopical Society, 97 (4), 502-511";
    // Strip HTML tags from the citation
    $citation = strip_tags($citation);
    // Initialize XMLCitation object
    $citationObj = new XMLCitation();
    // Initialize a cURL session
    $ch = curl_init();

    // Set the URL for the request
    $url = 'http://llama3.vliz.be:8070/api/processCitation';
    curl_setopt($ch, CURLOPT_URL, $url);

    // Set the request method to POST
    curl_setopt($ch, CURLOPT_POST, true);

    // Set the request headers
    $headers = array(
        'Content-Type: application/x-www-form-urlencoded'
    );
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    // Form data to be sent
    $citation = urlencode($citation); // Assuming $citation is the citation variable
    $postData = 'citations=' . $citation;

    // Set the form data to be sent
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

    // Return the transfer as a string
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // Execute the cURL session and store the response in a variable
    $response = curl_exec($ch);

    // Check if any error occurred
    if(curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    } else {
        // Print the response
        echo $response;
    }

    // Close the cURL session
    curl_close($ch);

    // Print the response for debugging
    echo $response;