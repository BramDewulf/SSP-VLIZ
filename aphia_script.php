<?php
//$citation = []
class Citation{
function freeciteCitation($citation, $return = "query") {
        
    $citation = "Kinahan, J.R. 1859a. List of Crustacea inhabiting Belfast Bay.-- Report of the 1858 Meeting of the British Association for the Advancement of Science 28: 291-293.";
    require_once 'vliz/class.httprequest.php';
    // Initialize HttpRequest
    $httpReq = new HttpRequest();

    // Initialize XMLCitation object
    $citationObj = new XMLCitation();

    // API URL
    $url = "http://llama3.vliz.be:8070/api/processCitation";

    // Set up request parameters, strip HTML tags
    $params['citation'] = strip_tags($citation);

    // Headers
    $headers = [
        // 'Accept' => 'text/xml',
        'Content-type' => 'application/x-www-form-urlencoded'
    ];

    // Send POST request
    $response = $httpReq->post($url, $params, $headers);
    echo($response);

    if (!empty($response)) {
        try {
            $response = new SimpleXMLElement($citationObj::stripControlChars($response));
        } catch (Exception $e) {
            aphiaLog("Failed to create SimpleXMLElement: $e \n Citation: $citation", basename(__FILE__, '.php'));
            return '';
        }
        $xml = simplexml_load_string($response);
        $authorForename = $xml->xpath("//author/persName/forename[@type='first']");
        $authorSurname = $xml->xpath("//author/persName/surname");
        $authors = [];
        foreach ($authorForenames as $index => $authorForename) {
            $authorSurname = isset($authorSurnames[$index]) ? $authorSurnames[$index] : ''; // if author string empty
            $authors[] = "{$authorForename} {$authorSurname}";
        }
        $authors = $xml->xpath("//title[@type='main']");
        $journal = $xml->xpath("//title[@level='j']")[0];
        $title = $xml->xpath("//title[@type='main']")[0];
        $year = $xml->xpath("//imprint/date[@type='published']");
        // Extract and combine suffix elements (volume, page, note)
        $volume = $xml->xpath("//imprint/biblScope[@unit='volume']");
        $pages = $xml->xpath("//imprint/biblScope[@unit='page']");
        $notes = $xml->xpath("//note");

        $suffixArray = [];

        // Add volume if exists
        if (!empty($volume)) {
            $suffixArray[] = "Volume: " . (string)$volume[0];
        }

        // Add pages if exists
        if (!empty($pages)) {
            $pageInfo = "Pages: ";
            $from = (string)$pages[0]['from'];
            $to = (string)$pages[0]['to'];
            $pageInfo .= $from;
            if (!empty($to)) {
                $pageInfo .= "-$to";
            }
            $suffixArray[] = $pageInfo;
        }

        // Add notes if exists
        if (!empty($notes)) {
            foreach ($notes as $note) {
                $suffixArray[] = "Note: " . (string)$note;
            }
        }

        // Combine all suffix parts into a single string
        $suffix = implode(', ', $suffixArray);
    }
     

}
}