import { createReducer } from 'redux-act';

import {
  resultLoadStart, resultLoadError, updateResults, updateExpandResults,
} from 'src/reducers/util';

import {
  queryCollections,
  queryDiagrams,
  queryRoles,
  queryEntities,
  queryEntityExpand,
  queryNotifications,
  queryCollectionXref,
} from 'src/actions';

const initialState = {};

export default createReducer({

  [queryCollections.START]: (state, { query }) => resultLoadStart(state, query),

  [queryCollections.ERROR]:
    (state, { error, args: { query } }) => resultLoadError(state, query, error),

  [queryCollections.COMPLETE]: updateResults,

  [queryEntities.START]: (state, { query }) => resultLoadStart(state, query),

  [queryEntities.ERROR]:
    (state, { error, args: { query } }) => resultLoadError(state, query, error),

  [queryEntities.COMPLETE]: updateResults,

  [queryEntityExpand.START]: (state, { query }) => resultLoadStart(state, query),

  [queryEntityExpand.ERROR]:
    (state, { error, args: { query } }) => resultLoadError(state, query, error),

  [queryEntityExpand.COMPLETE]: updateExpandResults,

  [queryNotifications.START]: (state, { query }) => resultLoadStart(state, query),

  [queryNotifications.ERROR]:
    (state, { error, args: { query } }) => resultLoadError(state, query, error),

  [queryNotifications.COMPLETE]: updateResults,

  [queryDiagrams.START]: (state, { query }) => resultLoadStart(state, query),

  [queryDiagrams.ERROR]: (state, {
    error, args: { query },
  }) => resultLoadError(state, query, error),

  [queryDiagrams.COMPLETE]: updateResults,

  [queryCollectionXref.COMPLETE]: updateResults,

  [queryCollectionXref.START]: (state, { query }) => resultLoadStart(state, query),

  [queryCollectionXref.ERROR]: (state, {
    error, args: { query },
  }) => resultLoadError(state, query, error),

  [queryRoles.COMPLETE]: updateResults,

  [queryRoles.START]: (state, { query }) => resultLoadStart(state, query),

  [queryRoles.ERROR]: (state, {
    error, args: { query },
  }) => resultLoadError(state, query, error),

}, initialState);
