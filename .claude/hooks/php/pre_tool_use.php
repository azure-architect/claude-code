#!/usr/bin/env php
<?php

function validatePHPFile($filePath, $content) {
    $issues = [];
    
    // Check max file length
    if (count(explode("\n", $content)) > 500) {
        $issues[] = "File exceeds 500 lines maximum length";
    }
    
    // Check for security issues
    if (strpos($content, 'eval(') !== false) {
        $issues[] = "Avoid using eval() - it's a security risk";
    }
    
    if (strpos($content, '$_GET') !== false || strpos($content, '$_POST') !== false) {
        if (strpos($content, 'filter_input') === false && strpos($content, 'htmlspecialchars') === false) {
            $issues[] = "Sanitize user input from \$_GET/\$_POST using filter_input() or htmlspecialchars()";
        }
    }
    
    // Check for SQL injection risks
    if (strpos($content, 'mysql_query') !== false) {
        $issues[] = "Use PDO or mysqli prepared statements instead of mysql_query()";
    }
    
    // Check for proper error handling
    if (strpos($content, 'die(') !== false || strpos($content, 'exit(') !== false) {
        $issues[] = "Consider using proper error handling instead of die()/exit()";
    }
    
    // Check for basic PHP opening tag
    if (!preg_match('/^<\?php/', $content)) {
        $issues[] = "PHP files should start with <?php opening tag";
    }
    
    // Check for short PHP tags
    if (strpos($content, '<?') !== false && strpos($content, '<?php') === false) {
        $issues[] = "Use full <?php opening tags instead of short tags";
    }
    
    return $issues;
}

function validateFile($filePath, $content) {
    $ext = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));
    
    if ($ext === 'php') {
        return validatePHPFile($filePath, $content);
    }
    
    return [];
}

try {
    $input = '';
    while (!feof(STDIN)) {
        $input .= fread(STDIN, 1024);
    }
    
    $inputData = json_decode($input, true);
    $toolName = $inputData['tool_name'] ?? '';
    $toolInput = $inputData['tool_input'] ?? [];
    
    $filePath = '';
    $content = '';
    
    if ($toolName === 'Write') {
        $filePath = $toolInput['file_path'] ?? '';
        $content = $toolInput['content'] ?? '';
    } elseif ($toolName === 'Edit') {
        $filePath = $toolInput['file_path'] ?? '';
        $content = $toolInput['new_content'] ?? '';
    }
    
    if ($filePath) {
        $issues = validateFile($filePath, $content);
        
        if (!empty($issues)) {
            fwrite(STDERR, "PHP file validation issues:\n");
            foreach ($issues as $issue) {
                fwrite(STDERR, "- $issue\n");
            }
            exit(2); // Block with feedback
        }
    }
    
    exit(0); // No issues
} catch (Exception $e) {
    fwrite(STDERR, "Hook error: " . $e->getMessage() . "\n");
    exit(1); // Non-blocking error
}
?>