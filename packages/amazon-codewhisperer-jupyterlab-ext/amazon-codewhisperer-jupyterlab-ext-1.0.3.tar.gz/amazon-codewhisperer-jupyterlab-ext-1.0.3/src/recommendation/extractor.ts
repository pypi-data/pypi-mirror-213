/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { NotebookPanel } from '@jupyterlab/notebook';
import { ICellModel } from '@jupyterlab/cells';
import { FileContext } from '../client/codewhispererclient'

import { FileContextMetadata } from "../utils/models";

import { Logger } from '../logging/logger';
import { pino } from 'pino';

import { MAX_LENGTH } from '../utils/constants'
import { CodeEditor } from '@jupyterlab/codeeditor';

const logger: pino.Logger = Logger.getInstance({
    "name": "codewhisperer",
    "component": "extractor"
});

/* This function serialized a notebook cell
* For markdown cell, convert it into python comment per line
* For code cell, send it as it is
* Add a \n between each cell
* Add one more \n after markdown cell, this is to let model know markdown has finished.
*/
function encodeCell(cell: ICellModel): string {
    if (cell.type === 'code') {
        return cell.toJSON()['source'] + '\n';
    } else if (cell.type === 'markdown') {
        const src = cell.toJSON()['source']
        let lines: string[] = []
        if (Array.isArray(src)) {
            lines = src
        } else {
            lines = src.split('\n')
        }
        return '# ' + lines.join('\n# ') + '\n\n';
    }
    return "";
}

export function isNotebookEmpty(panel: NotebookPanel): boolean {
    const cells = panel.content.model.cells;
    for (let i = 0; i < cells.length; i++) {
        const cell = cells.get(i);
        const src = cell.toJSON()['source'] as string
        if (src.trim() !== '') {
            return false
        }
    }
    return true
}

export function getFileContextFromNotebook(panel: NotebookPanel): {
    fileContext: FileContext | undefined;
    fileContextMetadata: FileContextMetadata;
} {
    const notebook = panel.content;
    const activeCell = notebook.activeCell;
    const editor = notebook.activeCell?.editor;
    const cellCount = notebook.model.cells.length;
    const cellType = activeCell.model.type;
    const lineNumber = editor?.getCursorPosition().line;
    const cursorOffset = editor?.getOffsetAt(editor.getCursorPosition());
    let fileContext = undefined;
    if (editor && activeCell) {
        const cells = notebook.model.cells;
        let left = ``;
        let right = ``;
        for (let i = 0; i < cells.length; i++) {
            const cell = cells.get(i);
            if (i < notebook.activeCellIndex) {
                left += encodeCell(cell);
            } else if (i === notebook.activeCellIndex) {
                const pos = editor.getCursorPosition();
                const offset = editor.getOffsetAt(pos);
                const text = editor.model.value.text;
                left += text.substring(0, offset);
                right += text.substring(offset, text.length);
            } else {
                right += encodeCell(cell);
            }
        }
        logger.debug(`Notebook content length - left:${left.slice.length} right:${left.slice.length}`)
        fileContext = {
            leftFileContent: left.slice(-MAX_LENGTH),
            rightFileContent: right.slice(0, MAX_LENGTH),
            filename: panel.context.path.split("/").pop(),
            programmingLanguage: {
                languageName: "python",
            }
        }
    }
    return {
        fileContext: fileContext,
        fileContextMetadata: {
            activeCellIdx: notebook.activeCellIndex,
            cellCount: cellCount,
            cellType: cellType,
            lineNumber: lineNumber,
            cursorOffset: cursorOffset,
        }
    };
}

export function getFileContextFromEditor(
    editor: CodeEditor.IEditor,
    filename: string
): {
    fileContext: FileContext | undefined;
    fileContextMetadata: FileContextMetadata;
} {
    let fileContext = undefined;
    let pos = undefined;
    let offset = undefined;
    if (editor) {
        pos = editor.getCursorPosition();
        offset = editor.getOffsetAt(pos);
        const text = editor.model.value.text;
        const left = text.substring(0, offset);
        const right = text.substring(offset, text.length);
        logger.debug(`File content length - left:${left.slice.length} right:${left.slice.length}`)
        fileContext = {
            leftFileContent: left.slice(-MAX_LENGTH),
            rightFileContent: right.slice(0, MAX_LENGTH),
            filename: filename,
            programmingLanguage: {
                languageName: "python",
            },
        }
    }
    return {
        fileContext: fileContext,
        fileContextMetadata: {
            lineNumber: pos.line,
            cursorOffset: offset,
        }
    };
}
