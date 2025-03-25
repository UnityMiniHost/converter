Error.stackTraceLimit = Infinity;

GameGlobal.oldFetch = GameGlobal.fetch;
if (!GameGlobal.oldFetch) {
    throw new Error('fetch is not defined');
}
GameGlobal.fetch = undefined; // remove fetch to follow wx
