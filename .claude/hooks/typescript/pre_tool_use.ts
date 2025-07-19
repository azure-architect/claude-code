#!/usr/bin/env ts-node

import * as fs from 'fs';

interface ToolInput {
    tool_name?: string;
    tool_input?: {
        file_path?: string;
        content?: string;
        new_content?: string;
    };
}

function validateTypeScriptFile(filePath: string, content: string): string[] {
    const issues: string[] = [];
    
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
    
    // Check for any type usage (should avoid)
    if (content.includes(': any') || content.includes('<any>')) {
        issues.push("Avoid using 'any' type - use specific types for better type safety");
    }
    
    // Check for console.log in production-like files
    if (filePath.includes('prod') && content.includes('console.log(')) {
        issues.push("Remove console.log statements from production code");
    }
    
    // Check for var usage (prefer const/let)
    if (content.includes('var ') && !content.includes('// allow-var')) {
        issues.push("Prefer const/let over var for block scoping");
    }
    
    // Check for basic interface/type definitions
    if (content.includes('interface') || content.includes('type ')) {
        // Good TypeScript practices
    }
    
    // Check for function return types
    if (content.includes('function ') && !content.match(/function\s+\w+\([^)]*\):\s*\w+/)) {
        issues.push("Functions should have explicit return type annotations");
    }
    
    return issues;
}

function validateFile(filePath: string, content: string): string[] {
    const ext = filePath.split('.').pop()?.toLowerCase();
    
    if (ext === 'ts' || ext === 'tsx') {
        return validateTypeScriptFile(filePath, content);
    }
    
    return [];
}

try {
    let input = '';
    process.stdin.on('data', (chunk) => input += chunk);
    process.stdin.on('end', () => {
        const inputData: ToolInput = JSON.parse(input);
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
                console.error('TypeScript file validation issues:');
                issues.forEach(issue => console.error(`- ${issue}`));
                process.exit(2); // Block with feedback
            }
        }
        
        process.exit(0); // No issues
    });
} catch (error) {
    console.error(`Hook error: ${(error as Error).message}`);
    process.exit(1); // Non-blocking error
}