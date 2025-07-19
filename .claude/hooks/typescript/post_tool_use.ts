#!/usr/bin/env ts-node

import { execSync } from 'child_process';
import * as fs from 'fs';

interface ToolInput {
    tool_name?: string;
    tool_input?: {
        file_path?: string;
        edits?: Array<{ file_path?: string }>;
    };
}

function formatTypeScriptFile(filePath: string): string | null {
    try {
        // Check if prettier is available
        try {
            execSync('which prettier', { stdio: 'ignore' });
        } catch {
            return 'Prettier not found. Install with: npm install -g prettier';
        }
        
        // Run prettier formatter
        execSync(`prettier --write "${filePath}"`, { stdio: 'pipe' });
        
        // Check if TypeScript compiler is available
        try {
            execSync('which tsc', { stdio: 'ignore' });
            const tscResult = execSync(`tsc --noEmit "${filePath}"`, { 
                encoding: 'utf8',
                stdio: 'pipe' 
            });
            
            if (tscResult.trim()) {
                return `TypeScript compilation issues:\n${tscResult}`;
            }
        } catch (tscError: any) {
            // TypeScript found issues
            if (tscError.status === 1) {
                return `TypeScript compilation issues:\n${tscError.stdout}`;
            }
            // tsc not installed - that's ok for formatting
        }
        
        // Check if ESLint is available for TypeScript linting
        try {
            execSync('which eslint', { stdio: 'ignore' });
            const eslintResult = execSync(`eslint "${filePath}"`, { 
                encoding: 'utf8',
                stdio: 'pipe' 
            });
            
            if (eslintResult.trim()) {
                return `ESLint issues:\n${eslintResult}`;
            }
        } catch (eslintError: any) {
            // ESLint found issues or not installed
            if (eslintError.status === 1) {
                return `ESLint issues:\n${eslintError.stdout}`;
            }
            // ESLint not installed - that's ok, just skip
        }
        
        return null;
    } catch (error) {
        return `Error formatting ${filePath}: ${(error as Error).message}`;
    }
}

function processFile(filePath: string): string | null {
    const ext = filePath.split('.').pop()?.toLowerCase();
    
    if (ext === 'ts' || ext === 'tsx') {
        return formatTypeScriptFile(filePath);
    }
    
    return null;
}

try {
    let input = '';
    process.stdin.on('data', (chunk) => input += chunk);
    process.stdin.on('end', () => {
        const inputData: ToolInput = JSON.parse(input);
        const toolName = inputData.tool_name || '';
        const toolInput = inputData.tool_input || {};
        
        let filePath = '';
        
        if (toolName === 'Write') {
            filePath = toolInput.file_path || '';
        } else if (toolName === 'Edit') {
            filePath = toolInput.file_path || '';
        } else if (toolName === 'MultiEdit') {
            const edits = toolInput.edits || [];
            if (edits.length > 0 && edits[0].file_path) {
                filePath = edits[0].file_path;
            }
        }
        
        if (filePath) {
            const issues = processFile(filePath);
            if (issues) {
                const jsonResponse = {
                    decision: 'block',
                    reason: `TypeScript file formatting issues detected:\n${issues}\nPlease fix these issues before proceeding.`
                };
                console.log(JSON.stringify(jsonResponse));
                process.exit(0); // Use exit code 0 with JSON response
            }
        }
        
        process.exit(0); // No issues
    });
} catch (error) {
    console.error(`Hook error: ${(error as Error).message}`);
    process.exit(1); // Non-blocking error
}