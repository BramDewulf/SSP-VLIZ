<!-- Script used for GROBID implementation obn Aphia codebase, only used as example, not functional  -->
 
<?php
/**
 * PHP implementation for GROBID API. Written by Bram Dewulf for VLIZ, requires marinespecies.og codebase to function
 *
 * @param string      $citation citation that needs to be parsed by the API.
 * @param string      $return   "query" text or "array"
 *
 * @return string always returns a query.
 */
function grobidCitation($citation, $return = "query") {
    require_once 'vliz/class.httprequest.php';
    global $aphia;
    $url = $aphia->grobid_link;
    $httpReq = new HttpRequest();
    $citationObj = new XMLCitation();
    // Encode the citation
    $citation = strip_tags($citation);
    $citation = urlencode($citation);
    $postData = 'citations=' . $citation;

    $headers = ['Content-type' => 'application/x-www-form-urlencoded; charset=utf-8'];
    $response = $httpReq->post($url, $postData, $headers);

    if (empty($response)) {
        return handleNoResponse($return);
    }

    try {
        $xml = new SimpleXMLElement($response);
    } catch (Exception $e) {
        aphiaLog("Failed to create SimpleXMLElement: $e \n Citation: $citation", basename(__FILE__, '.php'));
        return handleError($return);
    }

    // Extract metadata using XPath
    $metadata = extractMetadata($xml);

    // Process metadata
    $authors = processAuthors($metadata['authorNodes']);
    $journal = processJournal($metadata['journalNodes']);
    $title = processTitle($metadata['titleNodes']);

    // Special case for journal and title
    $journal = adjustJournalForSpecialCase($xml, $title, $journal);

    $year = processYear($metadata['yearNode']);
    $suffix = processSuffix($metadata['volumeNode'], $metadata['issueNode'], $metadata['pagesNode']);

    if ($return == "array") {
        return buildArrayResponse($authors, $title, $journal, $year, $suffix);
    } else {
        return buildQueryResponse($authors, $journal, $title, $year, $suffix);
    }
}

//Start GROBID functions
function handleNoResponse($return) {
    if ($return == "array") {
        return ['error' => 'No response from GROBID: please complete the fields manually'];
    }
    return '';
}

function handleError($return) {
    if ($return == "array") {
        return ['error' => 'GROBID could not parse the response: please complete the fields manually'];
    }
    return '';
}

function extractMetadata($xml) {
    return [
        'authorNodes' => $xml->xpath("//author/persName"),
        'journalNodes' => $xml->xpath("//title[@level='j'] | //title[@level='s']"),
        'titleNodes' => $xml->xpath("//title[@type='main'] | //title[@type='m'] | //title[@level='main'] | //title[@level='m'] | //title"),
        'yearNode' => $xml->xpath("//imprint/date[@type='published']"),
        'volumeNode' => $xml->xpath("//imprint/biblScope[@unit='volume']"),
        'issueNode' => $xml->xpath("//imprint/biblScope[@unit='issue']"),
        'pagesNode' => $xml->xpath("//imprint/biblScope[@unit='page']")
    ];
}

function processAuthors($authorNodes) {
    $authors = [];

    foreach ($authorNodes as $authorNode) {
        $forename = (string)$authorNode->xpath("forename[@type='first']")[0];
        $middleName = (string)$authorNode->xpath("forename[@type='middle']")[0];
        $surname = (string)$authorNode->xpath("surname")[0];

        if (!empty($surname)) {
            $forenameInitial = !empty($forename) ? substr($forename, 0, 1) . '.' : '';
            $middleNameInitial = !empty($middleName) ? ' ' . substr($middleName, 0, 1) . '.' : '';
            
            if (!empty($forenameInitial) || !empty($middleNameInitial)) {
                $authorName = "{$surname}, {$forenameInitial}{$middleNameInitial}";
            } else {
                $authorName = $surname;
            }
            
            $authors[] = trim($authorName);
        }
    }

    return implode('; ', $authors);
}

function processJournal($journalNodes) {
    return !empty($journalNodes) ? (string)$journalNodes[0] : '';
}

function processTitle($titleNodes) {
    return !empty($titleNodes) ? (string)$titleNodes[0] : '';
}
//Sometimes there is a special case in xml structure where the journal has level 'm' instead of 'j', only when title was already parsed
function adjustJournalForSpecialCase($xml, $title, $journal) {
    if (!empty($title) && $title !== (string)$xml->xpath("//title[@level='m']")[0]) {
        $journalNode = $xml->xpath("//title[@level='m']");
        if (!empty($journalNode)) {
            $journal = (string)$journalNode[0];
        }
    }
    return $journal;
}

function processYear($yearNode) {
    if (!empty($yearNode)) {
        $dateString = (string)$yearNode[0];
        if (preg_match('/\b(\d{4})\b/', $dateString, $matches)) {
            return rtrim($matches[1], '.');
        }
    }
    return '';
}

function processSuffix($volumeNode, $issueNode, $pagesNode) {
    $volume = !empty($volumeNode) ? (string)$volumeNode[0] : '';
    $issue = !empty($issueNode) ? (string)$issueNode[0] : '';
    $pageStr = '';

    if (!empty($pagesNode)) {
        $from = (string)$pagesNode[0]['from'];
        $to = (string)$pagesNode[0]['to'];
        if (!empty($from) && !empty($to)) {
            $pageStr = "$from-$to";
        } elseif (!empty($from)) {
            $pageStr = $from;
        } elseif (!empty($to)) {
            $pageStr = $to;
        } else {
            $pageStr = (string)$pagesNode[0];
        }
    }

    $issueStr = !empty($issue) ? "($issue)" : '';
    $separator = (!empty($volume) || !empty($issue)) && !empty($pageStr) ? ": " : '';

    // Return formatted volume and issue without additional trimming
    if (empty($pageStr)) {
        return trim("$volume$issueStr");
    }

    return trim("$volume$issueStr$separator$pageStr");
}

function buildArrayResponse($authors, $title, $journal, $year, $suffix) {
    if ($authors && $year && $title) {
        return [
            'author' => $authors,
            'title' => $title,
            'journal' => $journal,
            'year' => $year,
            'suffix' => $suffix
        ];
    } else {
        return ['error' => 'GROBID could not properly parse this citation: please complete the fields manually'];
    }
}

function buildQueryResponse($authors, $journal, $title, $year, $suffix) {
    $query = '';
    if ($authors && $year && $title && $journal) {
        $authors = eq($authors);
        $journal = eq($journal);
        $title = eq($title);
        $year = eq($year);
        $suffix = eq($suffix);
        $query = "UPDATE sources SET source_author = $authors, source_journal = $journal, source_title = $title, source_year = $year, source_suffix=$suffix ";
    }
    return $query;
}
//End GROBID functions