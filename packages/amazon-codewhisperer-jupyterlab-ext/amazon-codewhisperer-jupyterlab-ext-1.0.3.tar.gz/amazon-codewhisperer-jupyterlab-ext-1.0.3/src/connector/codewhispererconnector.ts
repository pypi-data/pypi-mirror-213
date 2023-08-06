/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { DataConnector } from '@jupyterlab/statedb';
import { CompletionHandler } from '@jupyterlab/completer';
import { NotebookPanel } from '@jupyterlab/notebook';

/**
 * A custom connector for completion handlers.
 */
export class CodeWhispererConnector extends DataConnector<
  CompletionHandler.ICompletionItemsReply,
  void,
  CompletionHandler.IRequest
> implements CompletionHandler.ICompletionItemsConnector {

  responseType = "ICompletionItemsReply" as const;
  /**
   * Create a new custom connector for completion requests.
   *
   * @param options - The instatiation options for the custom connector.
   */
  constructor(options: CodeWhispererConnector.IOptions) {
    super();
    this._notebookPanel = options.notebookPanel;
  }

  /**
   * Fetch completion requests.
   *
   * @param request - The completion request text and details.
   * @returns Completion reply
   */
  fetch(
    request: CompletionHandler.IRequest
  ): Promise<CompletionHandler.ICompletionItemsReply> {
    if (!this._notebookPanel) {
      return Promise.reject('No notebook');
    }
    return new Promise<CompletionHandler.ICompletionItemsReply>((resolve) => {
      resolve(this.getCompletions(this._notebookPanel));
    });
  }

  private _notebookPanel: NotebookPanel | null;

  async getCompletions(
    notebookPanel: NotebookPanel
  ): Promise<CompletionHandler.ICompletionItemsReply> {
    // Find the token at the cursor
    const editor = notebookPanel.content.activeCell?.editor;

    const cursor = editor.getCursorPosition();
    const offset = editor.getOffsetAt(cursor);

    const result: CompletionHandler.ICompletionItemsReply = {
      start: offset,
      end: offset,
      items: []
    }
    const items: CompletionHandler.ICompletionItem[] = []
    result.items = items
    return result;
  }



}

/**
 * A namespace for custom connector statics.
 */
export namespace CodeWhispererConnector {
  /**
   * The instantiation options for cell completion handlers.
   */
  export interface IOptions {
    /**
     * The session used by the custom connector.
     */
    notebookPanel: NotebookPanel | null;
  }
}



