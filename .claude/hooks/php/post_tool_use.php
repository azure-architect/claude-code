#!/usr/bin/env php
<?php

function formatPHPFile($filePath) {
    try {
        // Check if PHP-CS-Fixer is available
        $whichCmd = 'which php-cs-fixer 2>/dev/null';
        $result = shell_exec($whichCmd);
        
        if (empty($result)) {
            return 'PHP-CS-Fixer not found. Install with: composer global require friendsofphp/php-cs-fixer';
        }
        
        // Run PHP-CS-Fixer
        $fixerCmd = "php-cs-fixer fix \"$filePath\" --rules=@PSR12 2>&1";
        $fixerOutput = shell_exec($fixerCmd);
        
        // Check if PHPStan is available for static analysis
        $phpstanCmd = 'which phpstan 2>/dev/null';
        $phpstanResult = shell_exec($phpstanCmd);
        
        if (!empty($phpstanResult)) {
            $analysisCmd = "phpstan analyse \"$filePath\" --level=5 --no-progress --error-format=raw 2>&1";
            $analysisOutput = shell_exec($analysisCmd);
            
            if (!empty($analysisOutput) && strpos($analysisOutput, 'OK') === false) {
                return "PHPStan issues:\n$analysisOutput";
            }
        }
        
        // Basic syntax check
        $syntaxCmd = "php -l \"$filePath\" 2>&1";
        $syntaxOutput = shell_exec($syntaxCmd);
        
        if (strpos($syntaxOutput, 'No syntax errors') === false) {
            return "PHP syntax errors:\n$syntaxOutput";
        }
        
        return null;
    } catch (Exception $e) {
        return "Error formatting $filePath: " . $e->getMessage();
    }
}

function processFile($filePath) {
    $ext = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));
    
    if ($ext === 'php') {
        return formatPHPFile($filePath);
    }
    
    return null;
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
    
    if ($toolName === 'Write') {
        $filePath = $toolInput['file_path'] ?? '';
    } elseif ($toolName === 'Edit') {
        $filePath = $toolInput['file_path'] ?? '';
    } elseif ($toolName === 'MultiEdit') {
        $edits = $toolInput['edits'] ?? [];
        if (!empty($edits) && isset($edits[0]['file_path'])) {
            $filePath = $edits[0]['file_path'];
        }
    }
    
    if ($filePath) {
        $issues = processFile($filePath);
        if ($issues) {
            $jsonResponse = [
                'decision' => 'block',
                'reason' => "PHP file formatting issues detected:\n$issues\nPlease fix these issues before proceeding."
            ];
            echo json_encode($jsonResponse);
            exit(0); // Use exit code 0 with JSON response
        }
    }
    
    exit(0); // No issues
} catch (Exception $e) {
    fwrite(STDERR, "Hook error: " . $e->getMessage() . "\n");
    exit(1); // Non-blocking error
}
?>