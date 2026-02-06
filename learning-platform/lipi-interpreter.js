// Native JavaScript Lipi-Lang Interpreter
// Implements core Lipi-lang features for browser execution without dependencies
// Supports Telugu and English keywords

const LipiInterpreter = (() => {
    'use strict';

    // Keyword mappings: Telugu <-> English
    const KEYWORDS = {
        // Print statements
        'చెప్పు': 'print',
        'print': 'print',
        
        // Conditionals
        'ఒకవేళ': 'if',
        'యెడల': 'if',
        'if': 'if',
        'లేకపోతే:': 'else:',
        'else:': 'else:',
        
        // Loops
        'వరకు': 'while',
        'while': 'while',
        'ప్రతి': 'for',
        'for': 'for',
        'లో': 'in',
        'in': 'in',
        
        // Block end
        'ముగింపు': 'end',
        'end': 'end',
        
        // Built-in functions
        'పరిధి': 'range',
        'range': 'range'
    };

    /**
     * Extract string literals from expression
     */
    function extractStrings(expr) {
        const strings = [];
        let processed = expr.replace(/(["'])((?:\\.|(?!\1).)*?)\1/g, (match, quote, content) => {
            strings.push(content); // Store content without quotes
            return `__STRING_${strings.length - 1}__`;
        });
        return { processed, strings };
    }

    /**
     * Restore string literals in a value
     */
    function restoreStrings(value, strings) {
        if (typeof value !== 'string') return value;
        
        strings.forEach((str, idx) => {
            value = value.replace(`__STRING_${idx}__`, str);
        });
        return value;
    }

    /**
     * Evaluate an expression safely
     */
    function evaluateExpression(expr, variables, strings = []) {
        expr = expr.trim();
        
        // Handle string placeholders
        if (expr.startsWith('__STRING_') && expr.endsWith('__')) {
            const idx = parseInt(expr.match(/__STRING_(\d+)__/)[1]);
            return strings[idx] || '';
        }
        
        // Handle string literals (if not already extracted)
        if (expr.startsWith('"') && expr.endsWith('"')) {
            return expr.slice(1, -1);
        }
        if (expr.startsWith("'") && expr.endsWith("'")) {
            return expr.slice(1, -1);
        }

        // Handle numbers
        if (/^-?\d+(\.\d+)?$/.test(expr)) {
            return parseFloat(expr);
        }

        // Handle variables
        if (/^[a-zA-Z_\u0C00-\u0C7F][a-zA-Z0-9_\u0C00-\u0C7F]*$/.test(expr)) {
            if (expr in variables) {
                return variables[expr];
            }
            throw new Error(`Variable '${expr}' is not defined`);
        }

        // Handle string concatenation with +
        if (expr.includes('+')) {
            return evaluateConcatenation(expr, variables, strings);
        }

        // Handle arithmetic operations
        if (expr.includes('-') || expr.includes('*') || expr.includes('/')) {
            return evaluateArithmetic(expr, variables);
        }

        // Handle comparison operations
        if (expr.includes('>=') || expr.includes('<=') || expr.includes('==') || 
            expr.includes('!=') || expr.includes('>') || expr.includes('<')) {
            return evaluateComparison(expr, variables, strings);
        }

        // Handle range() function
        if (expr.includes('పరిధి(') || expr.includes('range(')) {
            return evaluateRange(expr, variables, strings);
        }

        throw new Error(`Cannot evaluate expression: ${expr}`);
    }

    /**
     * Evaluate concatenation expressions
     */
    function evaluateConcatenation(expr, variables, strings) {
        // Split by + but be careful with string placeholders
        const parts = [];
        let current = '';
        let depth = 0;
        
        for (let i = 0; i < expr.length; i++) {
            const char = expr[i];
            if (char === '(' || char === '[') depth++;
            else if (char === ')' || char === ']') depth--;
            else if (char === '+' && depth === 0) {
                parts.push(current.trim());
                current = '';
                continue;
            }
            current += char;
        }
        if (current) parts.push(current.trim());
        
        let result = evaluateExpression(parts[0], variables, strings);
        
        for (let i = 1; i < parts.length; i++) {
            const val = evaluateExpression(parts[i], variables, strings);
            // Convert to string for concatenation
            result = String(result) + String(val);
        }
        return result;
    }

    /**
     * Evaluate arithmetic expressions
     */
    function evaluateArithmetic(expr, variables) {
        // Replace variables with their values
        let processed = expr;
        for (const [varName, value] of Object.entries(variables)) {
            const regex = new RegExp(`\\b${escapeRegex(varName)}\\b`, 'g');
            processed = processed.replace(regex, String(value));
        }

        // Safely evaluate arithmetic (no eval!)
        try {
            // Only allow numbers and basic operators
            if (!/^[\d\s+\-*/.()]+$/.test(processed)) {
                throw new Error('Invalid arithmetic expression');
            }
            return Function('"use strict"; return (' + processed + ')')();
        } catch (e) {
            throw new Error(`Arithmetic error: ${e.message}`);
        }
    }

    /**
     * Evaluate comparison expressions
     */
    function evaluateComparison(expr, variables, strings) {
        const operators = ['>=', '<=', '==', '!=', '>', '<'];
        
        for (const op of operators) {
            const opIndex = expr.indexOf(op);
            if (opIndex !== -1) {
                const left = expr.substring(0, opIndex).trim();
                const right = expr.substring(opIndex + op.length).trim();
                const leftVal = evaluateExpression(left, variables, strings);
                const rightVal = evaluateExpression(right, variables, strings);
                
                switch (op) {
                    case '>=': return leftVal >= rightVal;
                    case '<=': return leftVal <= rightVal;
                    case '==': return leftVal == rightVal;
                    case '!=': return leftVal != rightVal;
                    case '>': return leftVal > rightVal;
                    case '<': return leftVal < rightVal;
                }
            }
        }
        
        return false;
    }

    /**
     * Evaluate range() function
     */
    function evaluateRange(expr, variables, strings) {
        // Extract range(start, end) or పరిధి(start, end)
        const match = expr.match(/(?:పరిధి|range)\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)/);
        if (!match) {
            throw new Error('Invalid range syntax');
        }

        const start = Math.floor(evaluateExpression(match[1], variables, strings));
        const end = Math.floor(evaluateExpression(match[2], variables, strings));
        
        const result = [];
        for (let i = start; i < end; i++) {
            result.push(i);
        }
        return result;
    }

    /**
     * Escape special regex characters
     */
    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * Parse and execute Lipi code
     */
    function execute(code) {
        const lines = code.split('\n');
        const output = [];
        const variables = {};
        let lineIndex = 0;

        try {
            lineIndex = executeBlock(lines, 0, lines.length, variables, output);
        } catch (error) {
            return {
                output: output.join('\n'),
                error: error.message
            };
        }

        return {
            output: output.join('\n'),
            error: null
        };
    }

    /**
     * Execute a block of lines (supports nested blocks)
     */
    function executeBlock(lines, startIndex, endIndex, variables, output) {
        let i = startIndex;

        while (i < endIndex) {
            let line = lines[i].trim();
            
            // Skip empty lines and comments
            if (!line || line.startsWith('#')) {
                i++;
                continue;
            }

            // Normalize keywords - handle both Telugu and English
            // Replace Telugu keywords with English equivalents
            for (const [teluguKey, englishKey] of Object.entries(KEYWORDS)) {
                if (teluguKey !== englishKey) {
                    // Check if the line starts with this keyword
                    if (line.startsWith(teluguKey + ' ') || line.startsWith(teluguKey + ':') || line === teluguKey) {
                        line = line.replace(teluguKey, englishKey);
                    }
                }
            }

            // Handle print statements
            if (line.startsWith('print ')) {
                const expr = line.substring(6).trim();
                const { processed, strings } = extractStrings(expr);
                
                let value = evaluateExpression(processed, variables, strings);
                
                output.push(String(value));
                i++;
                continue;
            }

            // Handle variable assignment
            if (line.includes('=') && !line.includes('==')) {
                const eqIndex = line.indexOf('=');
                const varName = line.substring(0, eqIndex).trim();
                const expr = line.substring(eqIndex + 1).trim();
                
                const { processed, strings } = extractStrings(expr);
                let value = evaluateExpression(processed, variables, strings);
                
                variables[varName] = value;
                i++;
                continue;
            }

            // Handle if statements
            if (line.startsWith('if ')) {
                // Extract condition - remove both leading 'if ' and trailing ':'
                let condition = line.substring(3).trim();
                if (condition.endsWith(':')) {
                    condition = condition.slice(0, -1).trim();
                }
                
                const { ifEnd, elseIndex } = findBlockEnd(lines, i);
                
                const { processed, strings } = extractStrings(condition);
                const conditionResult = evaluateExpression(processed, variables, strings);
                
                if (conditionResult) {
                    // Execute if block
                    const blockStart = i + 1;
                    const blockEnd = elseIndex !== -1 ? elseIndex : ifEnd;
                    executeBlock(lines, blockStart, blockEnd, variables, output);
                } else if (elseIndex !== -1) {
                    // Execute else block
                    executeBlock(lines, elseIndex + 1, ifEnd, variables, output);
                }
                
                i = ifEnd + 1;
                continue;
            }

            // Handle while loops
            if (line.startsWith('while ')) {
                // Extract condition - remove both leading 'while ' and trailing ':'
                let condition = line.substring(6).trim();
                if (condition.endsWith(':')) {
                    condition = condition.slice(0, -1).trim();
                }
                
                const loopEnd = findLoopEnd(lines, i);
                
                const maxIterations = 10000; // Prevent infinite loops
                let iterations = 0;
                
                while (true) {
                    if (iterations++ > maxIterations) {
                        throw new Error('Infinite loop detected (max 10000 iterations)');
                    }
                    
                    const { processed, strings } = extractStrings(condition);
                    if (!evaluateExpression(processed, variables, strings)) {
                        break;
                    }
                    
                    executeBlock(lines, i + 1, loopEnd, variables, output);
                }
                
                i = loopEnd + 1;
                continue;
            }

            // Handle for loops
            if (line.startsWith('for ')) {
                const forMatch = line.match(/for\s+(\S+)\s+in\s+(.+):?/);
                if (!forMatch) {
                    throw new Error('Invalid for loop syntax');
                }
                
                const loopVar = forMatch[1];
                let iterableExpr = forMatch[2].trim();
                if (iterableExpr.endsWith(':')) {
                    iterableExpr = iterableExpr.slice(0, -1).trim();
                }
                
                const loopEnd = findLoopEnd(lines, i);
                
                const { processed, strings } = extractStrings(iterableExpr);
                const iterable = evaluateExpression(processed, variables, strings);
                
                if (!Array.isArray(iterable)) {
                    throw new Error('For loop requires an iterable (array or range)');
                }
                
                for (const value of iterable) {
                    variables[loopVar] = value;
                    executeBlock(lines, i + 1, loopEnd, variables, output);
                }
                
                i = loopEnd + 1;
                continue;
            }

            // Unknown statement
            throw new Error(`Unknown statement: ${line}`);
        }

        return i;
    }

    /**
     * Find the end of an if-else block
     */
    function findBlockEnd(lines, startIndex) {
        let depth = 0;
        let elseIndex = -1;
        
        for (let i = startIndex; i < lines.length; i++) {
            let line = lines[i].trim();
            
            if (!line || line.startsWith('#')) continue;
            
            // Normalize keywords
            for (const [teluguKey, englishKey] of Object.entries(KEYWORDS)) {
                if (teluguKey !== englishKey) {
                    if (line.startsWith(teluguKey + ' ') || line.startsWith(teluguKey + ':') || line === teluguKey) {
                        line = line.replace(teluguKey, englishKey);
                    }
                }
            }
            
            if (line.startsWith('if ') || line.startsWith('while ') || line.startsWith('for ')) {
                depth++;
            } else if (line === 'end') {
                if (depth === 1) {
                    return { ifEnd: i, elseIndex };
                }
                depth--;
            } else if (line === 'else:' && depth === 1) {
                elseIndex = i;
            }
        }
        
        throw new Error('Missing "end" or "ముగింపు" keyword');
    }

    /**
     * Find the end of a loop block
     */
    function findLoopEnd(lines, startIndex) {
        let depth = 0;
        
        for (let i = startIndex; i < lines.length; i++) {
            let line = lines[i].trim();
            
            if (!line || line.startsWith('#')) continue;
            
            // Normalize keywords
            for (const [teluguKey, englishKey] of Object.entries(KEYWORDS)) {
                if (teluguKey !== englishKey) {
                    if (line.startsWith(teluguKey + ' ') || line.startsWith(teluguKey + ':') || line === teluguKey) {
                        line = line.replace(teluguKey, englishKey);
                    }
                }
            }
            
            if (line.startsWith('if ') || line.startsWith('while ') || line.startsWith('for ')) {
                depth++;
            } else if (line === 'end') {
                if (depth === 1) {
                    return i;
                }
                depth--;
            }
        }
        
        throw new Error('Missing "end" or "ముగింపు" keyword');
    }

    // Public API
    return {
        execute
    };
})();
