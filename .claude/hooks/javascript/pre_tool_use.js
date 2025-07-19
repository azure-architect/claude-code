#!/usr/bin/env node

const fs = require('fs');

function validateJavaScriptFile(filePath, content) {
    const issues = [];
    
    // Check max file length
    if (content.split('\n').length > 500) {
        issues.push("File exceeds 500 lines maximum length");
    }
    
    // Check for security issues
    if (content.includes('eval(')) {
        issues.push("Avoid using eval() - it's a security risk");
    }
    
    if (content.includes('innerHTML') && !content.includes('sanitize')) {
        issues.push("Use innerHTML with caution - consider sanitizing input");
    }
    
    // Check for console.log in production-like files
    if (filePath.includes('prod') && content.includes('console.log(')) {
        issues.push("Remove console.log statements from production code");
    }
    
    // Check for basic function structure
    if (content.includes('function') || content.includes('=>')) {
        // Basic function checks passed
    }
    
    // Check for var usage (prefer const/let)
    if (content.includes('var ') && !content.includes('// allow-var')) {
        issues.push("Prefer const/let over var for block scoping");
    }
    
    return issues;
}

function validateFile(filePath, content) {
    const ext = filePath.split('.').pop().toLowerCase();
    
    if (ext === 'js' || ext === 'jsx') {
        return validateJavaScriptFile(filePath, content);
    }
    
    return [];
}

try {
    let input = '';
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', () => {
        const inputData = JSON.parse(input);
        const toolName = inputData.tool_name || '';
        const toolInput = inputData.tool_input || {};
        
        let filePath = '';
        let content = '';
        
        if (toolName === 'Write') {
            filePath = toolInput.file_path || '';
            content = toolInput.content || '';
        } else if (toolName === 'Edit') {
            filePath = toolInput.file_path || '';
            content = toolInput.new_content || '';
        }
        
        if (filePath) {
            const issues = validateFile(filePath, content);
            
            if (issues.length > 0) {
                console.error('JavaScript file validation issues:');
                issues.forEach(issue => console.error(`- ${issue}`));
                process.exit(2); // Block with feedback
            }
        }
        
        process.exit(0); // No issues
    });
} catch (error) {
    console.error(`Hook error: ${error.message}`);
    process.exit(1); // Non-blocking error
}