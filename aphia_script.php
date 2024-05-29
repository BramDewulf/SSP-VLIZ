<?php
$citation = []
class Citation {
    function sendCitationToApi($citation) {
        require_once 'vliz/class.httprequest.php';
        // Initialize HttpRequest
        $httpReq = new HttpRequest();

        // Initialize XMLCitation object
        $citationObj = new XMLCitation();

        // API URL
        $url = "http://freecite.library.brown.edu/citations/create";

        // Set up request parameters, strip HTML tags
        $params['citation'] = strip_tags($citation);

        // Headers
        $headers = [
            'Accept' => 'text/xml',
            'Content-type' => 'application/x-www-form-urlencoded; charset=utf-8'
        ];

        // Send POST request
        $response = $httpReq->post($url, $params, $headers);
        echo($response)

    }
}