/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { DataConnector } from '@jupyterlab/statedb';
import { CompletionHandler } from '@jupyterlab/completer';

/**
 * A multi-connector connector for completion handlers.
 */
export class MergeConnector extends DataConnector<
  CompletionHandler.ICompletionItemsReply,
  void,
  CompletionHandler.IRequest
> implements CompletionHandler.ICompletionItemsConnector{
  responseType = "ICompletionItemsReply" as const;

  completionItemsConnector: CompletionHandler.ICompletionItemsConnector;

  kernelConnector: DataConnector<
    CompletionHandler.IReply,
    void,
    CompletionHandler.IRequest
  >;
  
  contextConnector: DataConnector<
  CompletionHandler.IReply,
  void,
  CompletionHandler.IRequest
>;

  constructor(
    completionItemsConnector?: CompletionHandler.ICompletionItemsConnector,
    kernelConnector?: DataConnector<
      CompletionHandler.IReply,
      void,
      CompletionHandler.IRequest
    >,
    contextConnector?: DataConnector<
      CompletionHandler.IReply,
      void,
      CompletionHandler.IRequest
    >
  ) {
    super();
    this.completionItemsConnector = completionItemsConnector;
    this.kernelConnector = kernelConnector;
    this.contextConnector = contextConnector;
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

    return Promise.all([
      this.completionItemsConnector.fetch(request),
      this.kernelConnector.fetch(request),
      this.contextConnector.fetch(request),
    ]).then(([replyWithItems, replyWithMatches]) => {
      return Private.mergeReplies(replyWithItems, replyWithMatches);
    });
  }
}

/**
 * A namespace for private functionality.
 */
namespace Private {
  
export function mergeReplies(
  replyWithItems: CompletionHandler.ICompletionItemsReply,
  replyWithMatches: CompletionHandler.IReply
): CompletionHandler.ICompletionItemsReply {
  const { start } = replyWithItems;
  const { end } = replyWithItems;
  const items: CompletionHandler.ICompletionItem[] = [];
  replyWithItems.items.forEach((item) => items.push(item));

  const replyWithMatchesMetaData = replyWithMatches.metadata
    ._jupyter_types_experimental as Array<{ type: string }>;

  replyWithMatches.matches.forEach((label, index) =>
    items.push({
      label,
      type: replyWithMatchesMetaData
        ? replyWithMatchesMetaData[index].type
        : "",
    })
  );

  return { start, items, end };
}
}
