var _self = "undefined" !== typeof window ? window : "undefined" !== typeof WorkerGlobalScope && self instanceof WorkerGlobalScope ? self : {},
    Prism = function () {
        var b = /\blang(?:uage)?-([\w-]+)\b/i,
            e = 0,
            c = _self.Prism = {
                manual: _self.Prism && _self.Prism.manual,
                disableWorkerMessageHandler: _self.Prism && _self.Prism.disableWorkerMessageHandler,
                util: {
                    encode: function (a) {
                        return a instanceof d ? new d(a.type, c.util.encode(a.content), a.alias) : "Array" === c.util.type(a) ? a.map(c.util.encode) : a.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\u00a0/g,
                            " ")
                    },
                    type: function (a) {
                        return Object.prototype.toString.call(a).match(/\[object (\w+)\]/)[1]
                    },
                    objId: function (a) {
                        a.__id || Object.defineProperty(a, "__id", {
                            value: ++e
                        });
                        return a.__id
                    },
                    clone: function (a, f) {
                        var g = c.util.type(a);
                        f = f || {};
                        switch (g) {
                            case "Object":
                                if (f[c.util.objId(a)]) return f[c.util.objId(a)];
                                var b = {};
                                f[c.util.objId(a)] = b;
                                for (var d in a) a.hasOwnProperty(d) && (b[d] = c.util.clone(a[d], f));
                                return b;
                            case "Array":
                                if (f[c.util.objId(a)]) return f[c.util.objId(a)];
                                b = [];
                                f[c.util.objId(a)] = b;
                                a.forEach(function (a,
                                    g) {
                                    b[g] = c.util.clone(a, f)
                                });
                                return b
                        }
                        return a
                    }
                },
                languages: {
                    extend: function (a, f) {
                        a = c.util.clone(c.languages[a]);
                        for (var g in f) a[g] = f[g];
                        return a
                    },
                    insertBefore: function (a, f, g, b) {
                        b = b || c.languages;
                        var l = b[a];
                        if (2 == arguments.length) {
                            g = arguments[1];
                            for (var d in g) g.hasOwnProperty(d) && (l[d] = g[d]);
                            return l
                        }
                        var e = {},
                            k;
                        for (k in l)
                            if (l.hasOwnProperty(k)) {
                                if (k == f)
                                    for (d in g) g.hasOwnProperty(d) && (e[d] = g[d]);
                                e[k] = l[k]
                            } c.languages.DFS(c.languages, function (f, c) {
                            c === b[a] && f != a && (this[f] = e)
                        });
                        return b[a] = e
                    },
                    DFS: function (a,
                        f, g, b) {
                        b = b || {};
                        for (var d in a) a.hasOwnProperty(d) && ((f.call(a, d, a[d], g || d), "Object" !== c.util.type(a[d]) || b[c.util.objId(a[d])]) ? "Array" !== c.util.type(a[d]) || b[c.util.objId(a[d])] || (b[c.util.objId(a[d])] = !0, c.languages.DFS(a[d], f, d, b)) : (b[c.util.objId(a[d])] = !0, c.languages.DFS(a[d], f, null, b)))
                    }
                },
                plugins: {},
                highlightAll: function (a, f) {
                    c.highlightAllUnder(document, a, f)
                },
                highlightAllUnder: function (a, f, b) {
                    b = {
                        callback: b,
                        selector: 'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'
                    };
                    c.hooks.run("before-highlightall", b);
                    a = b.elements || a.querySelectorAll(b.selector);
                    for (var g = 0, d; d = a[g++];) c.highlightElement(d, !0 === f, b.callback)
                },
                highlightElement: function (a, f, g) {
                    for (var d, e, k = a; k && !b.test(k.className);) k = k.parentNode;
                    k && (d = (k.className.match(b) || [, ""])[1].toLowerCase(), e = c.languages[d]);
                    a.className = a.className.replace(b, "").replace(/\s+/g, " ") + " language-" + d;
                    a.parentNode && (k = a.parentNode, /pre/i.test(k.nodeName) && (k.className = k.className.replace(b, "").replace(/\s+/g, " ") + " language-" +
                        d));
                    var h = {
                        element: a,
                        language: d,
                        grammar: e,
                        code: a.textContent
                    };
                    c.hooks.run("before-sanity-check", h);
                    h.code && h.grammar ? (c.hooks.run("before-highlight", h), f && _self.Worker ? (a = new Worker(c.filename), a.onmessage = function (a) {
                        h.highlightedCode = a.data;
                        c.hooks.run("before-insert", h);
                        h.element.innerHTML = h.highlightedCode;
                        g && g.call(h.element);
                        c.hooks.run("after-highlight", h);
                        c.hooks.run("complete", h)
                    }, a.postMessage(JSON.stringify({
                        language: h.language,
                        code: h.code,
                        immediateClose: !0
                    }))) : (h.highlightedCode = c.highlight(h.code,
                        h.grammar, h.language), c.hooks.run("before-insert", h), h.element.innerHTML = h.highlightedCode, g && g.call(a), c.hooks.run("after-highlight", h), c.hooks.run("complete", h))) : (h.code && (c.hooks.run("before-highlight", h), h.element.textContent = h.code, c.hooks.run("after-highlight", h)), c.hooks.run("complete", h))
                },
                highlight: function (a, b, g) {
                    a = {
                        code: a,
                        grammar: b,
                        language: g
                    };
                    c.hooks.run("before-tokenize", a);
                    a.tokens = c.tokenize(a.code, a.grammar);
                    c.hooks.run("after-tokenize", a);
                    return d.stringify(c.util.encode(a.tokens),
                        a.language)
                },
                matchGrammar: function (a, b, g, d, e, k, h) {
                    var f = c.Token,
                        l;
                    for (l in g)
                        if (g.hasOwnProperty(l) && g[l]) {
                            if (l == h) break;
                            var r = g[l];
                            r = "Array" === c.util.type(r) ? r : [r];
                            for (var w = 0; w < r.length; ++w) {
                                var p = r[w],
                                    B = p.inside,
                                    C = !!p.lookbehind,
                                    z = !!p.greedy,
                                    A = 0,
                                    D = p.alias;
                                if (z && !p.pattern.global) {
                                    var q = p.pattern.toString().match(/[imuy]*$/)[0];
                                    p.pattern = RegExp(p.pattern.source, q + "g")
                                }
                                p = p.pattern || p;
                                q = d;
                                for (var u = e; q < b.length; u += b[q].length, ++q) {
                                    var n = b[q];
                                    if (b.length > a.length) return;
                                    if (!(n instanceof f)) {
                                        if (z &&
                                            q != b.length - 1) {
                                            p.lastIndex = u;
                                            var m = p.exec(a);
                                            if (!m) break;
                                            var v = m.index + (C ? m[1].length : 0),
                                                y = m.index + m[0].length,
                                                t = q;
                                            n = u;
                                            for (var E = b.length; t < E && (n < y || !b[t].type && !b[t - 1].greedy); ++t) n += b[t].length, v >= n && (++q, u = n);
                                            if (b[q] instanceof f) continue;
                                            t -= q;
                                            n = a.slice(u, n);
                                            m.index -= u
                                        } else p.lastIndex = 0, m = p.exec(n), t = 1;
                                        m && (C && (A = m[1] ? m[1].length : 0), v = m.index + A, m = m[0].slice(A), y = v + m.length, v = n.slice(0, v), y = n.slice(y), n = [q, t], v && (++q, u += v.length, n.push(v)), m = new f(l, B ? c.tokenize(m, B) : m, D, m, z), n.push(m), y && n.push(y),
                                            Array.prototype.splice.apply(b, n), 1 != t && c.matchGrammar(a, b, g, q, u, !0, l));
                                        if (k) break
                                    }
                                }
                            }
                        }
                },
                tokenize: function (a, b, d) {
                    d = [a];
                    var f = b.rest;
                    if (f) {
                        for (var g in f) b[g] = f[g];
                        delete b.rest
                    }
                    c.matchGrammar(a, d, b, 0, 0, !1);
                    return d
                },
                hooks: {
                    all: {},
                    add: function (a, b) {
                        var d = c.hooks.all;
                        d[a] = d[a] || [];
                        d[a].push(b)
                    },
                    run: function (a, b) {
                        if ((a = c.hooks.all[a]) && a.length)
                            for (var d = 0, f; f = a[d++];) f(b)
                    }
                }
            },
            d = c.Token = function (a, b, d, c, e) {
                this.type = a;
                this.content = b;
                this.alias = d;
                this.length = (c || "").length | 0;
                this.greedy = !!e
            };
        d.stringify =
            function (a, b, g) {
                if ("string" == typeof a) return a;
                if ("Array" === c.util.type(a)) return a.map(function (c) {
                    return d.stringify(c, b, a)
                }).join("");
                var f = {
                    type: a.type,
                    content: d.stringify(a.content, b, g),
                    tag: "span",
                    classes: ["token", a.type],
                    attributes: {},
                    language: b,
                    parent: g
                };
                a.alias && (g = "Array" === c.util.type(a.alias) ? a.alias : [a.alias], Array.prototype.push.apply(f.classes, g));
                c.hooks.run("wrap", f);
                g = Object.keys(f.attributes).map(function (a) {
                    return a + '="' + (f.attributes[a] || "").replace(/"/g, "&quot;") + '"'
                }).join(" ");
                return "<" + f.tag + ' class="' + f.classes.join(" ") + '"' + (g ? " " + g : "") + ">" + f.content + "</" + f.tag + ">"
            };
        if (!_self.document) {
            if (!_self.addEventListener) return _self.Prism;
            c.disableWorkerMessageHandler || _self.addEventListener("message", function (a) {
                a = JSON.parse(a.data);
                var b = a.language,
                    d = a.immediateClose;
                _self.postMessage(c.highlight(a.code, c.languages[b], b));
                d && _self.close()
            }, !1);
            return _self.Prism
        }
        var k = document.currentScript || [].slice.call(document.getElementsByTagName("script")).pop();
        k && (c.filename = k.src,
            c.manual || k.hasAttribute("data-manual") || ("loading" !== document.readyState ? window.requestAnimationFrame ? window.requestAnimationFrame(c.highlightAll) : window.setTimeout(c.highlightAll, 16) : document.addEventListener("DOMContentLoaded", c.highlightAll)));
        return _self.Prism
    }();
"undefined" !== typeof module && module.exports && (module.exports = Prism);
"undefined" !== typeof global && (global.Prism = Prism);
Prism.languages.markup = {
    comment: /\x3c!--[\s\S]*?--\x3e/,
    prolog: /<\?[\s\S]+?\?>/,
    doctype: /<!DOCTYPE[\s\S]+?>/i,
    cdata: /<!\[CDATA\[[\s\S]*?]]\x3e/i,
    tag: {
        pattern: /<\/?(?!\d)[^\s>\/=$<%]+(?:\s+[^\s>\/=]+(?:=(?:("|')(?:\\[\s\S]|(?!\1)[^\\])*\1|[^\s'">=]+))?)*\s*\/?>/i,
        greedy: !0,
        inside: {
            tag: {
                pattern: /^<\/?[^\s>\/]+/i,
                inside: {
                    punctuation: /^<\/?/,
                    namespace: /^[^\s>\/:]+:/
                }
            },
            "attr-value": {
                pattern: /=(?:("|')(?:\\[\s\S]|(?!\1)[^\\])*\1|[^\s'">=]+)/i,
                inside: {
                    punctuation: [/^=/, {
                        pattern: /(^|[^\\])["']/,
                        lookbehind: !0
                    }]
                }
            },
            punctuation: /\/?>/,
            "attr-name": {
                pattern: /[^\s>\/]+/,
                inside: {
                    namespace: /^[^\s>\/:]+:/
                }
            }
        }
    },
    entity: /&#?[\da-z]{1,8};/i
};
Prism.languages.markup.tag.inside["attr-value"].inside.entity = Prism.languages.markup.entity;
Prism.hooks.add("wrap", function (b) {
    "entity" === b.type && (b.attributes.title = b.content.replace(/&amp;/, "&"))
});
Prism.languages.xml = Prism.languages.markup;
Prism.languages.html = Prism.languages.markup;
Prism.languages.mathml = Prism.languages.markup;
Prism.languages.svg = Prism.languages.markup;
Prism.languages.css = {
    comment: /\/\*[\s\S]*?\*\//,
    atrule: {
        pattern: /@[\w-]+?.*?(?:;|(?=\s*\{))/i,
        inside: {
            rule: /@[\w-]+/
        }
    },
    url: /url\((?:(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1|.*?)\)/i,
    selector: /[^{}\s][^{};]*?(?=\s*\{)/,
    string: {
        pattern: /("|')(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
        greedy: !0
    },
    property: /[-_a-z\xA0-\uFFFF][-\w\xA0-\uFFFF]*(?=\s*:)/i,
    important: /\B!important\b/i,
    "function": /[-a-z0-9]+(?=\()/i,
    punctuation: /[(){};:]/
};
Prism.languages.css.atrule.inside.rest = Prism.languages.css;
Prism.languages.markup && (Prism.languages.insertBefore("markup", "tag", {
    style: {
        pattern: /(<style[\s\S]*?>)[\s\S]*?(?=<\/style>)/i,
        lookbehind: !0,
        inside: Prism.languages.css,
        alias: "language-css",
        greedy: !0
    }
}), Prism.languages.insertBefore("inside", "attr-value", {
        "style-attr": {
            pattern: /\s*style=("|')(?:\\[\s\S]|(?!\1)[^\\])*\1/i,
            inside: {
                "attr-name": {
                    pattern: /^\s*style/i,
                    inside: Prism.languages.markup.tag.inside
                },
                punctuation: /^\s*=\s*['"]|['"]\s*$/,
                "attr-value": {
                    pattern: /.+/i,
                    inside: Prism.languages.css
                }
            },
            alias: "language-css"
        }
    },
    Prism.languages.markup.tag));
Prism.languages.clike = {
    comment: [{
        pattern: /(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/,
        lookbehind: !0
    }, {
        pattern: /(^|[^\\:])\/\/.*/,
        lookbehind: !0,
        greedy: !0
    }],
    string: {
        pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
        greedy: !0
    },
    "class-name": {
        pattern: /((?:\b(?:class|interface|extends|implements|trait|instanceof|new)\s+)|(?:catch\s+\())[\w.\\]+/i,
        lookbehind: !0,
        inside: {
            punctuation: /[.\\]/
        }
    },
    keyword: /\b(?:if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue)\b/,
    "boolean": /\b(?:true|false)\b/,
    "function": /[a-z0-9_]+(?=\()/i,
    number: /\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?/i,
    operator: /--?|\+\+?|!=?=?|<=?|>=?|==?=?|&&?|\|\|?|\?|\*|\/|~|\^|%/,
    punctuation: /[{}[\];(),.:]/
};
Prism.languages.javascript = Prism.languages.extend("clike", {
    keyword: /\b(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield)\b/,
    object: /\b(?:ActiveXObject|Array|Audio|Boolean|Date|Debug|Enumerator|Error|FileReader|Function|Global|Image|JSON|Math|Number|Object|Option|RegExp|String|VBArray|arguments|WebSocket|Worker|XMLHttpRequest|window|document|options|console|_this|that|result)\b/,
    number: /\b(?:0[xX][\dA-Fa-f]+|0[bB][01]+|0[oO][0-7]+|NaN|Infinity)\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee][+-]?\d+)?/,
    "function": /[_$a-z\xA0-\uFFFF][$\w\xA0-\uFFFF]*(?=\s*\()/i,
    operator: /-[-=]?|\+[+=]?|!=?=?|<<?=?|>>?>?=?|=(?:==?|>)?|&[&=]?|\|[|=]?|\*\*?=?|\/=?|~|\^=?|%=?|\?|\$|\.{3}/
});
Prism.languages.insertBefore("javascript", "keyword", {
    regex: {
        pattern: /((?:^|[^$\w\xA0-\uFFFF."'\])\s])\s*)\/(\[[^\]\r\n]+]|\\.|[^/\\\[\r\n])+\/[gimyu]{0,5}(?=\s*($|[\r\n,.})\]]))/,
        lookbehind: !0,
        greedy: !0
    },
    "function-variable": {
        pattern: /[_$a-z\xA0-\uFFFF][$\w\xA0-\uFFFF]*(?=\s*=\s*(?:function\b|(?:\([^()]*\)|[_$a-z\xA0-\uFFFF][$\w\xA0-\uFFFF]*)\s*=>))/i,
        alias: "function"
    },
    constant: /\b[A-Z][A-Z\d_]*\b/
});
Prism.languages.insertBefore("javascript", "string", {
    "template-string": {
        pattern: /`(?:\\[\s\S]|\${[^}]+}|[^\\`])*`/,
        greedy: !0,
        inside: {
            interpolation: {
                pattern: /\${[^}]+}/,
                inside: {
                    "interpolation-punctuation": {
                        pattern: /^\${|}$/,
                        alias: "punctuation"
                    },
                    rest: null
                }
            },
            string: /[\s\S]+/
        }
    }
});
Prism.languages.javascript["template-string"].inside.interpolation.inside.rest = Prism.languages.javascript;
Prism.languages.markup && Prism.languages.insertBefore("markup", "tag", {
    script: {
        pattern: /(<script[\s\S]*?>)[\s\S]*?(?=<\/script>)/i,
        lookbehind: !0,
        inside: Prism.languages.javascript,
        alias: "language-javascript",
        greedy: !0
    }
});
Prism.languages.js = Prism.languages.javascript;
Prism.languages.apacheconf = {
    comment: /#.*/,
    "directive-inline": {
        pattern: /^(\s*)\b(?:AcceptFilter|AcceptPathInfo|AccessFileName|Action|AddAlt|AddAltByEncoding|AddAltByType|AddCharset|AddDefaultCharset|AddDescription|AddEncoding|AddHandler|AddIcon|AddIconByEncoding|AddIconByType|AddInputFilter|AddLanguage|AddModuleInfo|AddOutputFilter|AddOutputFilterByType|AddType|Alias|AliasMatch|Allow|AllowCONNECT|AllowEncodedSlashes|AllowMethods|AllowOverride|AllowOverrideList|Anonymous|Anonymous_LogEmail|Anonymous_MustGiveEmail|Anonymous_NoUserID|Anonymous_VerifyEmail|AsyncRequestWorkerFactor|AuthBasicAuthoritative|AuthBasicFake|AuthBasicProvider|AuthBasicUseDigestAlgorithm|AuthDBDUserPWQuery|AuthDBDUserRealmQuery|AuthDBMGroupFile|AuthDBMType|AuthDBMUserFile|AuthDigestAlgorithm|AuthDigestDomain|AuthDigestNonceLifetime|AuthDigestProvider|AuthDigestQop|AuthDigestShmemSize|AuthFormAuthoritative|AuthFormBody|AuthFormDisableNoStore|AuthFormFakeBasicAuth|AuthFormLocation|AuthFormLoginRequiredLocation|AuthFormLoginSuccessLocation|AuthFormLogoutLocation|AuthFormMethod|AuthFormMimetype|AuthFormPassword|AuthFormProvider|AuthFormSitePassphrase|AuthFormSize|AuthFormUsername|AuthGroupFile|AuthLDAPAuthorizePrefix|AuthLDAPBindAuthoritative|AuthLDAPBindDN|AuthLDAPBindPassword|AuthLDAPCharsetConfig|AuthLDAPCompareAsUser|AuthLDAPCompareDNOnServer|AuthLDAPDereferenceAliases|AuthLDAPGroupAttribute|AuthLDAPGroupAttributeIsDN|AuthLDAPInitialBindAsUser|AuthLDAPInitialBindPattern|AuthLDAPMaxSubGroupDepth|AuthLDAPRemoteUserAttribute|AuthLDAPRemoteUserIsDN|AuthLDAPSearchAsUser|AuthLDAPSubGroupAttribute|AuthLDAPSubGroupClass|AuthLDAPUrl|AuthMerging|AuthName|AuthnCacheContext|AuthnCacheEnable|AuthnCacheProvideFor|AuthnCacheSOCache|AuthnCacheTimeout|AuthnzFcgiCheckAuthnProvider|AuthnzFcgiDefineProvider|AuthType|AuthUserFile|AuthzDBDLoginToReferer|AuthzDBDQuery|AuthzDBDRedirectQuery|AuthzDBMType|AuthzSendForbiddenOnFailure|BalancerGrowth|BalancerInherit|BalancerMember|BalancerPersist|BrowserMatch|BrowserMatchNoCase|BufferedLogs|BufferSize|CacheDefaultExpire|CacheDetailHeader|CacheDirLength|CacheDirLevels|CacheDisable|CacheEnable|CacheFile|CacheHeader|CacheIgnoreCacheControl|CacheIgnoreHeaders|CacheIgnoreNoLastMod|CacheIgnoreQueryString|CacheIgnoreURLSessionIdentifiers|CacheKeyBaseURL|CacheLastModifiedFactor|CacheLock|CacheLockMaxAge|CacheLockPath|CacheMaxExpire|CacheMaxFileSize|CacheMinExpire|CacheMinFileSize|CacheNegotiatedDocs|CacheQuickHandler|CacheReadSize|CacheReadTime|CacheRoot|CacheSocache|CacheSocacheMaxSize|CacheSocacheMaxTime|CacheSocacheMinTime|CacheSocacheReadSize|CacheSocacheReadTime|CacheStaleOnError|CacheStoreExpired|CacheStoreNoStore|CacheStorePrivate|CGIDScriptTimeout|CGIMapExtension|CharsetDefault|CharsetOptions|CharsetSourceEnc|CheckCaseOnly|CheckSpelling|ChrootDir|ContentDigest|CookieDomain|CookieExpires|CookieName|CookieStyle|CookieTracking|CoreDumpDirectory|CustomLog|Dav|DavDepthInfinity|DavGenericLockDB|DavLockDB|DavMinTimeout|DBDExptime|DBDInitSQL|DBDKeep|DBDMax|DBDMin|DBDParams|DBDPersist|DBDPrepareSQL|DBDriver|DefaultIcon|DefaultLanguage|DefaultRuntimeDir|DefaultType|Define|DeflateBufferSize|DeflateCompressionLevel|DeflateFilterNote|DeflateInflateLimitRequestBody|DeflateInflateRatioBurst|DeflateInflateRatioLimit|DeflateMemLevel|DeflateWindowSize|Deny|DirectoryCheckHandler|DirectoryIndex|DirectoryIndexRedirect|DirectorySlash|DocumentRoot|DTracePrivileges|DumpIOInput|DumpIOOutput|EnableExceptionHook|EnableMMAP|EnableSendfile|Error|ErrorDocument|ErrorLog|ErrorLogFormat|Example|ExpiresActive|ExpiresByType|ExpiresDefault|ExtendedStatus|ExtFilterDefine|ExtFilterOptions|FallbackResource|FileETag|FilterChain|FilterDeclare|FilterProtocol|FilterProvider|FilterTrace|ForceLanguagePriority|ForceType|ForensicLog|GprofDir|GracefulShutdownTimeout|Group|Header|HeaderName|HeartbeatAddress|HeartbeatListen|HeartbeatMaxServers|HeartbeatStorage|HeartbeatStorage|HostnameLookups|IdentityCheck|IdentityCheckTimeout|ImapBase|ImapDefault|ImapMenu|Include|IncludeOptional|IndexHeadInsert|IndexIgnore|IndexIgnoreReset|IndexOptions|IndexOrderDefault|IndexStyleSheet|InputSed|ISAPIAppendLogToErrors|ISAPIAppendLogToQuery|ISAPICacheFile|ISAPIFakeAsync|ISAPILogNotSupported|ISAPIReadAheadBuffer|KeepAlive|KeepAliveTimeout|KeptBodySize|LanguagePriority|LDAPCacheEntries|LDAPCacheTTL|LDAPConnectionPoolTTL|LDAPConnectionTimeout|LDAPLibraryDebug|LDAPOpCacheEntries|LDAPOpCacheTTL|LDAPReferralHopLimit|LDAPReferrals|LDAPRetries|LDAPRetryDelay|LDAPSharedCacheFile|LDAPSharedCacheSize|LDAPTimeout|LDAPTrustedClientCert|LDAPTrustedGlobalCert|LDAPTrustedMode|LDAPVerifyServerCert|LimitInternalRecursion|LimitRequestBody|LimitRequestFields|LimitRequestFieldSize|LimitRequestLine|LimitXMLRequestBody|Listen|ListenBackLog|LoadFile|LoadModule|LogFormat|LogLevel|LogMessage|LuaAuthzProvider|LuaCodeCache|LuaHookAccessChecker|LuaHookAuthChecker|LuaHookCheckUserID|LuaHookFixups|LuaHookInsertFilter|LuaHookLog|LuaHookMapToStorage|LuaHookTranslateName|LuaHookTypeChecker|LuaInherit|LuaInputFilter|LuaMapHandler|LuaOutputFilter|LuaPackageCPath|LuaPackagePath|LuaQuickHandler|LuaRoot|LuaScope|MaxConnectionsPerChild|MaxKeepAliveRequests|MaxMemFree|MaxRangeOverlaps|MaxRangeReversals|MaxRanges|MaxRequestWorkers|MaxSpareServers|MaxSpareThreads|MaxThreads|MergeTrailers|MetaDir|MetaFiles|MetaSuffix|MimeMagicFile|MinSpareServers|MinSpareThreads|MMapFile|ModemStandard|ModMimeUsePathInfo|MultiviewsMatch|Mutex|NameVirtualHost|NoProxy|NWSSLTrustedCerts|NWSSLUpgradeable|Options|Order|OutputSed|PassEnv|PidFile|PrivilegesMode|Protocol|ProtocolEcho|ProxyAddHeaders|ProxyBadHeader|ProxyBlock|ProxyDomain|ProxyErrorOverride|ProxyExpressDBMFile|ProxyExpressDBMType|ProxyExpressEnable|ProxyFtpDirCharset|ProxyFtpEscapeWildcards|ProxyFtpListOnWildcard|ProxyHTMLBufSize|ProxyHTMLCharsetOut|ProxyHTMLDocType|ProxyHTMLEnable|ProxyHTMLEvents|ProxyHTMLExtended|ProxyHTMLFixups|ProxyHTMLInterp|ProxyHTMLLinks|ProxyHTMLMeta|ProxyHTMLStripComments|ProxyHTMLURLMap|ProxyIOBufferSize|ProxyMaxForwards|ProxyPass|ProxyPassInherit|ProxyPassInterpolateEnv|ProxyPassMatch|ProxyPassReverse|ProxyPassReverseCookieDomain|ProxyPassReverseCookiePath|ProxyPreserveHost|ProxyReceiveBufferSize|ProxyRemote|ProxyRemoteMatch|ProxyRequests|ProxySCGIInternalRedirect|ProxySCGISendfile|ProxySet|ProxySourceAddress|ProxyStatus|ProxyTimeout|ProxyVia|ReadmeName|ReceiveBufferSize|Redirect|RedirectMatch|RedirectPermanent|RedirectTemp|ReflectorHeader|RemoteIPHeader|RemoteIPInternalProxy|RemoteIPInternalProxyList|RemoteIPProxiesHeader|RemoteIPTrustedProxy|RemoteIPTrustedProxyList|RemoveCharset|RemoveEncoding|RemoveHandler|RemoveInputFilter|RemoveLanguage|RemoveOutputFilter|RemoveType|RequestHeader|RequestReadTimeout|Require|RewriteBase|RewriteCond|RewriteEngine|RewriteMap|RewriteOptions|RewriteRule|RLimitCPU|RLimitMEM|RLimitNPROC|Satisfy|ScoreBoardFile|Script|ScriptAlias|ScriptAliasMatch|ScriptInterpreterSource|ScriptLog|ScriptLogBuffer|ScriptLogLength|ScriptSock|SecureListen|SeeRequestTail|SendBufferSize|ServerAdmin|ServerAlias|ServerLimit|ServerName|ServerPath|ServerRoot|ServerSignature|ServerTokens|Session|SessionCookieName|SessionCookieName2|SessionCookieRemove|SessionCryptoCipher|SessionCryptoDriver|SessionCryptoPassphrase|SessionCryptoPassphraseFile|SessionDBDCookieName|SessionDBDCookieName2|SessionDBDCookieRemove|SessionDBDDeleteLabel|SessionDBDInsertLabel|SessionDBDPerUser|SessionDBDSelectLabel|SessionDBDUpdateLabel|SessionEnv|SessionExclude|SessionHeader|SessionInclude|SessionMaxAge|SetEnv|SetEnvIf|SetEnvIfExpr|SetEnvIfNoCase|SetHandler|SetInputFilter|SetOutputFilter|SSIEndTag|SSIErrorMsg|SSIETag|SSILastModified|SSILegacyExprParser|SSIStartTag|SSITimeFormat|SSIUndefinedEcho|SSLCACertificateFile|SSLCACertificatePath|SSLCADNRequestFile|SSLCADNRequestPath|SSLCARevocationCheck|SSLCARevocationFile|SSLCARevocationPath|SSLCertificateChainFile|SSLCertificateFile|SSLCertificateKeyFile|SSLCipherSuite|SSLCompression|SSLCryptoDevice|SSLEngine|SSLFIPS|SSLHonorCipherOrder|SSLInsecureRenegotiation|SSLOCSPDefaultResponder|SSLOCSPEnable|SSLOCSPOverrideResponder|SSLOCSPResponderTimeout|SSLOCSPResponseMaxAge|SSLOCSPResponseTimeSkew|SSLOCSPUseRequestNonce|SSLOpenSSLConfCmd|SSLOptions|SSLPassPhraseDialog|SSLProtocol|SSLProxyCACertificateFile|SSLProxyCACertificatePath|SSLProxyCARevocationCheck|SSLProxyCARevocationFile|SSLProxyCARevocationPath|SSLProxyCheckPeerCN|SSLProxyCheckPeerExpire|SSLProxyCheckPeerName|SSLProxyCipherSuite|SSLProxyEngine|SSLProxyMachineCertificateChainFile|SSLProxyMachineCertificateFile|SSLProxyMachineCertificatePath|SSLProxyProtocol|SSLProxyVerify|SSLProxyVerifyDepth|SSLRandomSeed|SSLRenegBufferSize|SSLRequire|SSLRequireSSL|SSLSessionCache|SSLSessionCacheTimeout|SSLSessionTicketKeyFile|SSLSRPUnknownUserSeed|SSLSRPVerifierFile|SSLStaplingCache|SSLStaplingErrorCacheTimeout|SSLStaplingFakeTryLater|SSLStaplingForceURL|SSLStaplingResponderTimeout|SSLStaplingResponseMaxAge|SSLStaplingResponseTimeSkew|SSLStaplingReturnResponderErrors|SSLStaplingStandardCacheTimeout|SSLStrictSNIVHostCheck|SSLUserName|SSLUseStapling|SSLVerifyClient|SSLVerifyDepth|StartServers|StartThreads|Substitute|Suexec|SuexecUserGroup|ThreadLimit|ThreadsPerChild|ThreadStackSize|TimeOut|TraceEnable|TransferLog|TypesConfig|UnDefine|UndefMacro|UnsetEnv|Use|UseCanonicalName|UseCanonicalPhysicalPort|User|UserDir|VHostCGIMode|VHostCGIPrivs|VHostGroup|VHostPrivs|VHostSecure|VHostUser|VirtualDocumentRoot|VirtualDocumentRootIP|VirtualScriptAlias|VirtualScriptAliasIP|WatchdogInterval|XBitHack|xml2EncAlias|xml2EncDefault|xml2StartParse)\b/mi,
        lookbehind: !0,
        alias: "property"
    },
    "directive-block": {
        pattern: /<\/?\b(?:AuthnProviderAlias|AuthzProviderAlias|Directory|DirectoryMatch|Else|ElseIf|Files|FilesMatch|If|IfDefine|IfModule|IfVersion|Limit|LimitExcept|Location|LocationMatch|Macro|Proxy|RequireAll|RequireAny|RequireNone|VirtualHost)\b *.*>/i,
        inside: {
            "directive-block": {
                pattern: /^<\/?\w+/,
                inside: {
                    punctuation: /^<\/?/
                },
                alias: "tag"
            },
            "directive-block-parameter": {
                pattern: /.*[^>]/,
                inside: {
                    punctuation: /:/,
                    string: {
                        pattern: /("|').*\1/,
                        inside: {
                            variable: /[$%]\{?(?:\w\.?[-+:]?)+\}?/
                        }
                    }
                },
                alias: "attr-value"
            },
            punctuation: />/
        },
        alias: "tag"
    },
    "directive-flags": {
        pattern: /\[(?:\w,?)+\]/,
        alias: "keyword"
    },
    string: {
        pattern: /("|').*\1/,
        inside: {
            variable: /[$%]\{?(?:\w\.?[-+:]?)+\}?/
        }
    },
    variable: /[$%]\{?(?:\w\.?[-+:]?)+\}?/,
    regex: /\^?.*\$|\^.*\$?/
};
Prism.languages.c = Prism.languages.extend("clike", {
    keyword: /\b(?:_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local|asm|typeof|inline|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b/,
    operator: /-[>-]?|\+\+?|!=?|<<?=?|>>?=?|==?|&&?|\|\|?|[~^%?*\/]/,
    number: /(?:\b0x[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?)[ful]*/i
});
Prism.languages.insertBefore("c", "string", {
    macro: {
        pattern: /(^\s*)#\s*[a-z]+(?:[^\r\n\\]|\\(?:\r\n|[\s\S]))*/im,
        lookbehind: !0,
        alias: "property",
        inside: {
            string: {
                pattern: /(#\s*include\s*)(?:<.+?>|("|')(?:\\?.)+?\2)/,
                lookbehind: !0
            },
            directive: {
                pattern: /(#\s*)\b(?:define|defined|elif|else|endif|error|ifdef|ifndef|if|import|include|line|pragma|undef|using)\b/,
                lookbehind: !0,
                alias: "keyword"
            }
        }
    },
    constant: /\b(?:__FILE__|__LINE__|__DATE__|__TIME__|__TIMESTAMP__|__func__|EOF|NULL|SEEK_CUR|SEEK_END|SEEK_SET|stdin|stdout|stderr)\b/
});
delete Prism.languages.c["class-name"];
delete Prism.languages.c["boolean"];
Prism.languages.aspnet = Prism.languages.extend("markup", {
    "page-directive tag": {
        pattern: /<%\s*@.*%>/i,
        inside: {
            "page-directive tag": /<%\s*@\s*(?:Assembly|Control|Implements|Import|Master(?:Type)?|OutputCache|Page|PreviousPageType|Reference|Register)?|%>/i,
            rest: Prism.languages.markup.tag.inside
        }
    },
    "directive tag": {
        pattern: /<%.*%>/i,
        inside: {
            "directive tag": /<%\s*?[$=%#:]{0,2}|%>/i,
            rest: Prism.languages.csharp
        }
    }
});
Prism.languages.aspnet.tag.pattern = /<(?!%)\/?[^\s>\/]+(?:\s+[^\s>\/=]+(?:=(?:("|')(?:\\[\s\S]|(?!\1)[^\\])*\1|[^\s'">=]+))?)*\s*\/?>/i;
Prism.languages.insertBefore("inside", "punctuation", {
    "directive tag": Prism.languages.aspnet["directive tag"]
}, Prism.languages.aspnet.tag.inside["attr-value"]);
Prism.languages.insertBefore("aspnet", "comment", {
    "asp comment": /<%--[\s\S]*?--%>/
});
Prism.languages.insertBefore("aspnet", Prism.languages.javascript ? "script" : "tag", {
    "asp script": {
        pattern: /(<script(?=.*runat=['"]?server['"]?)[\s\S]*?>)[\s\S]*?(?=<\/script>)/i,
        lookbehind: !0,
        inside: Prism.languages.csharp || {}
    }
});
(function (b) {
    var e = {
        variable: [{
            pattern: /\$?\(\([\s\S]+?\)\)/,
            inside: {
                variable: [{
                    pattern: /(^\$\(\([\s\S]+)\)\)/,
                    lookbehind: !0
                }, /^\$\(\(/],
                number: /\b0x[\dA-Fa-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?/,
                operator: /--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/=?|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:/,
                punctuation: /\(\(?|\)\)?|,|;/
            }
        }, {
            pattern: /\$\([^)]+\)|`[^`]+`/,
            greedy: !0,
            inside: {
                variable: /^\$\(|^`|\)$|`$/
            }
        }, /\$(?:[\w#?*!@]+|\{[^}]+\})/i]
    };
    b.languages.bash = {
        shebang: {
            pattern: /^#!\s*\/bin\/bash|^#!\s*\/bin\/sh/,
            alias: "important"
        },
        comment: {
            pattern: /(^|[^"{\\])#.*/,
            lookbehind: !0
        },
        string: [{
            pattern: /((?:^|[^<])<<\s*)["']?(\w+?)["']?\s*\r?\n(?:[\s\S])*?\r?\n\2/,
            lookbehind: !0,
            greedy: !0,
            inside: e
        }, {
            pattern: /(["'])(?:\\[\s\S]|\$\([^)]+\)|`[^`]+`|(?!\1)[^\\])*\1/,
            greedy: !0,
            inside: e
        }],
        variable: e.variable,
        "function": {
            pattern: /(^|[\s;|&])(?:alias|apropos|apt-get|aptitude|aspell|awk|basename|bash|bc|bg|builtin|bzip2|cal|cat|cd|cfdisk|chgrp|chmod|chown|chroot|chkconfig|cksum|clear|cmp|comm|command|cp|cron|crontab|csplit|curl|cut|date|dc|dd|ddrescue|df|diff|diff3|dig|dir|dircolors|dirname|dirs|dmesg|du|egrep|eject|enable|env|ethtool|eval|exec|expand|expect|export|expr|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|fuser|gawk|getopts|git|grep|groupadd|groupdel|groupmod|groups|gzip|hash|head|help|hg|history|hostname|htop|iconv|id|ifconfig|ifdown|ifup|import|install|jobs|join|kill|killall|less|link|ln|locate|logname|logout|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|make|man|mkdir|mkfifo|mkisofs|mknod|more|most|mount|mtools|mtr|mv|mmv|nano|netstat|nice|nl|nohup|notify-send|npm|nslookup|open|op|passwd|paste|pathchk|ping|pkill|popd|pr|printcap|printenv|printf|ps|pushd|pv|pwd|quota|quotacheck|quotactl|ram|rar|rcp|read|readarray|readonly|reboot|rename|renice|remsync|rev|rm|rmdir|rsync|screen|scp|sdiff|sed|seq|service|sftp|shift|shopt|shutdown|sleep|slocate|sort|source|split|ssh|stat|strace|su|sudo|sum|suspend|sync|tail|tar|tee|test|time|timeout|times|touch|top|traceroute|trap|tr|tsort|tty|type|ulimit|umask|umount|unalias|uname|unexpand|uniq|units|unrar|unshar|uptime|useradd|userdel|usermod|users|uuencode|uudecode|v|vdir|vi|vmstat|wait|watch|wc|wget|whereis|which|who|whoami|write|xargs|xdg-open|yes|zip)(?=$|[\s;|&])/,
            lookbehind: !0
        },
        keyword: {
            pattern: /(^|[\s;|&])(?:let|:|\.|if|then|else|elif|fi|for|break|continue|while|in|case|function|select|do|done|until|echo|exit|return|set|declare)(?=$|[\s;|&])/,
            lookbehind: !0
        },
        "boolean": {
            pattern: /(^|[\s;|&])(?:true|false)(?=$|[\s;|&])/,
            lookbehind: !0
        },
        operator: /&&?|\|\|?|==?|!=?|<<<?|>>|<=?|>=?|=~/,
        punctuation: /\$?\(\(?|\)\)?|\.\.|[{}[\];]/
    };
    e = e.variable[1].inside;
    e.string = b.languages.bash.string;
    e["function"] = b.languages.bash["function"];
    e.keyword = b.languages.bash.keyword;
    e["boolean"] =
        b.languages.bash["boolean"];
    e.operator = b.languages.bash.operator;
    e.punctuation = b.languages.bash.punctuation;
    b.languages.shell = b.languages.bash
})(Prism);
Prism.languages.cpp = Prism.languages.extend("c", {
    keyword: /\b(?:alignas|alignof|asm|auto|bool|break|case|catch|char|char16_t|char32_t|class|compl|const|constexpr|const_cast|continue|decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|extern|float|for|friend|goto|if|inline|int|int8_t|int16_t|int32_t|int64_t|uint8_t|uint16_t|uint32_t|uint64_t|long|mutable|namespace|new|noexcept|nullptr|operator|private|protected|public|register|reinterpret_cast|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|template|this|thread_local|throw|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while)\b/,
    "boolean": /\b(?:true|false)\b/,
    operator: /--?|\+\+?|!=?|<{1,2}=?|>{1,2}=?|->|:{1,2}|={1,2}|\^|~|%|&{1,2}|\|\|?|\?|\*|\/|\b(?:and|and_eq|bitand|bitor|not|not_eq|or|or_eq|xor|xor_eq)\b/
});
Prism.languages.insertBefore("cpp", "keyword", {
    "class-name": {
        pattern: /(class\s+)\w+/i,
        lookbehind: !0
    }
});
Prism.languages.insertBefore("cpp", "string", {
    "raw-string": {
        pattern: /R"([^()\\ ]{0,16})\([\s\S]*?\)\1"/,
        alias: "string",
        greedy: !0
    }
});
Prism.languages.csharp = Prism.languages.extend("clike", {
    keyword: /\b(?:abstract|add|alias|as|ascending|async|await|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|descending|do|double|dynamic|else|enum|event|explicit|extern|false|finally|fixed|float|for|foreach|from|get|global|goto|group|if|implicit|in|int|interface|internal|into|is|join|let|lock|long|namespace|new|null|object|operator|orderby|out|override|params|partial|private|protected|public|readonly|ref|remove|return|sbyte|sealed|select|set|short|sizeof|stackalloc|static|string|struct|switch|this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|value|var|virtual|void|volatile|where|while|yield)\b/,
    string: [{
        pattern: /@("|')(?:\1\1|\\[\s\S]|(?!\1)[^\\])*\1/,
        greedy: !0
    }, {
        pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*?\1/,
        greedy: !0
    }],
    "class-name": [{
        pattern: /\b[A-Z]\w*(?:\.\w+)*\b(?=\s+\w+)/,
        inside: {
            punctuation: /\./
        }
    }, {
        pattern: /(\[)[A-Z]\w*(?:\.\w+)*\b/,
        lookbehind: !0,
        inside: {
            punctuation: /\./
        }
    }, {
        pattern: /(\b(?:class|interface)\s+[A-Z]\w*(?:\.\w+)*\s*:\s*)[A-Z]\w*(?:\.\w+)*\b/,
        lookbehind: !0,
        inside: {
            punctuation: /\./
        }
    }, {
        pattern: /((?:\b(?:class|interface|new)\s+)|(?:catch\s+\())[A-Z]\w*(?:\.\w+)*\b/,
        lookbehind: !0,
        inside: {
            punctuation: /\./
        }
    }],
    number: /\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)f?/i
});
Prism.languages.insertBefore("csharp", "class-name", {
    "generic-method": {
        pattern: /\w+\s*<[^>\r\n]+?>\s*(?=\()/,
        inside: {
            function: /^\w+/,
            "class-name": {
                pattern: /\b[A-Z]\w*(?:\.\w+)*\b/,
                inside: {
                    punctuation: /\./
                }
            },
            keyword: Prism.languages.csharp.keyword,
            punctuation: /[<>(),.:]/
        }
    },
    preprocessor: {
        pattern: /(^\s*)#.*/m,
        lookbehind: !0,
        alias: "property",
        inside: {
            directive: {
                pattern: /(\s*#)\b(?:define|elif|else|endif|endregion|error|if|line|pragma|region|undef|warning)\b/,
                lookbehind: !0,
                alias: "keyword"
            }
        }
    }
});
Prism.languages.dotnet = Prism.languages.csharp;
(function (b) {
    var e = /#(?!\{).+/,
        c = {
            pattern: /#\{[^}]+\}/,
            alias: "variable"
        };
    b.languages.coffeescript = b.languages.extend("javascript", {
        comment: e,
        string: [{
            pattern: /'(?:\\[\s\S]|[^\\'])*'/,
            greedy: !0
        }, {
            pattern: /"(?:\\[\s\S]|[^\\"])*"/,
            greedy: !0,
            inside: {
                interpolation: c
            }
        }],
        keyword: /\b(?:and|break|by|catch|class|continue|debugger|delete|do|each|else|extend|extends|false|finally|for|if|in|instanceof|is|isnt|let|loop|namespace|new|no|not|null|of|off|on|or|own|return|super|switch|then|this|throw|true|try|typeof|undefined|unless|until|when|while|window|with|yes|yield)\b/,
        "class-member": {
            pattern: /@(?!\d)\w+/,
            alias: "variable"
        }
    });
    b.languages.insertBefore("coffeescript", "comment", {
        "multiline-comment": {
            pattern: /###[\s\S]+?###/,
            alias: "comment"
        },
        "block-regex": {
            pattern: /\/{3}[\s\S]*?\/{3}/,
            alias: "regex",
            inside: {
                comment: e,
                interpolation: c
            }
        }
    });
    b.languages.insertBefore("coffeescript", "string", {
        "inline-javascript": {
            pattern: /`(?:\\[\s\S]|[^\\`])*`/,
            inside: {
                delimiter: {
                    pattern: /^`|`$/,
                    alias: "punctuation"
                },
                rest: b.languages.javascript
            }
        },
        "multiline-string": [{
            pattern: /'''[\s\S]*?'''/,
            greedy: !0,
            alias: "string"
        }, {
            pattern: /"""[\s\S]*?"""/,
            greedy: !0,
            alias: "string",
            inside: {
                interpolation: c
            }
        }]
    });
    b.languages.insertBefore("coffeescript", "keyword", {
        property: /(?!\d)\w+(?=\s*:(?!:))/
    });
    delete b.languages.coffeescript["template-string"]
})(Prism);
Prism.languages["markup-templating"] = {};
Object.defineProperties(Prism.languages["markup-templating"], {
    buildPlaceholders: {
        value: function (b, e, c, d) {
            b.language === e && (b.tokenStack = [], b.code = b.code.replace(c, function (c) {
                if ("function" === typeof d && !d(c)) return c;
                for (var a = b.tokenStack.length; - 1 !== b.code.indexOf("___" + e.toUpperCase() + a + "___");) ++a;
                b.tokenStack[a] = c;
                return "___" + e.toUpperCase() + a + "___"
            }), b.grammar = Prism.languages.markup)
        }
    },
    tokenizePlaceholders: {
        value: function (b, e) {
            if (b.language === e && b.tokenStack) {
                b.grammar = Prism.languages[e];
                var c =
                    0,
                    d = Object.keys(b.tokenStack),
                    k = function (a) {
                        if (!(c >= d.length))
                            for (var f = 0; f < a.length; f++) {
                                var g = a[f];
                                if ("string" === typeof g || g.content && "string" === typeof g.content) {
                                    var l = d[c],
                                        r = b.tokenStack[l],
                                        w = "string" === typeof g ? g : g.content,
                                        h = w.indexOf("___" + e.toUpperCase() + l + "___");
                                    if (-1 < h) {
                                        ++c;
                                        var x = w.substring(0, h);
                                        r = new Prism.Token(e, Prism.tokenize(r, b.grammar, e), "language-" + e, r);
                                        l = w.substring(h + ("___" + e.toUpperCase() + l + "___").length);
                                        x || l ? (x = [x, r, l].filter(function (a) {
                                            return !!a
                                        }), k(x)) : x = r;
                                        "string" === typeof g ?
                                            Array.prototype.splice.apply(a, [f, 1].concat(x)) : g.content = x;
                                        if (c >= d.length) break
                                    }
                                } else g.content && "string" !== typeof g.content && k(g.content)
                            }
                    };
                k(b.tokens)
            }
        }
    }
});
Prism.languages.git = {
    comment: /^#.*/m,
    deleted: /^[-\u00e2\u20ac\u201c].*/m,
    inserted: /^\+.*/m,
    string: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/m,
    command: {
        pattern: /^.*\$ git .*$/m,
        inside: {
            parameter: /\s--?\w+/m
        }
    },
    coord: /^@@.*@@$/m,
    commit_sha1: /^commit \w{40}$/m
};
Prism.languages.java = Prism.languages.extend("clike", {
    keyword: /\b(?:abstract|continue|for|new|switch|assert|default|goto|package|synchronized|boolean|do|if|private|this|break|double|implements|protected|throw|byte|else|import|public|throws|case|enum|instanceof|return|transient|catch|extends|int|short|try|char|final|interface|static|void|class|finally|long|strictfp|volatile|const|float|native|super|while)\b/,
    number: /\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?/i,
    operator: {
        pattern: /(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/=?|%=?|\^=?|[?:~])/m,
        lookbehind: !0
    }
});
Prism.languages.insertBefore("java", "function", {
    annotation: {
        alias: "punctuation",
        pattern: /(^|[^.])@\w+/,
        lookbehind: !0
    }
});
Prism.languages.insertBefore("java", "class-name", {
    generics: {
        pattern: /<\s*\w+(?:\.\w+)?(?:\s*,\s*\w+(?:\.\w+)?)*>/i,
        alias: "function",
        inside: {
            keyword: Prism.languages.java.keyword,
            punctuation: /[<>(),.:]/
        }
    }
});
Prism.languages.less = Prism.languages.extend("css", {
    comment: [/\/\*[\s\S]*?\*\//, {
        pattern: /(^|[^\\])\/\/.*/,
        lookbehind: !0
    }],
    atrule: {
        pattern: /@[\w-]+?(?:\([^{}]+\)|[^(){};])*?(?=\s*\{)/i,
        inside: {
            punctuation: /[:()]/
        }
    },
    selector: {
        pattern: /(?:@\{[\w-]+\}|[^{};\s@])(?:@\{[\w-]+\}|\([^{}]*\)|[^{};@])*?(?=\s*\{)/,
        inside: {
            variable: /@+[\w-]+/
        }
    },
    property: /(?:@\{[\w-]+\}|[\w-])+(?:\+_?)?(?=\s*:)/i,
    punctuation: /[{}();:,]/,
    operator: /[+\-*\/]/
});
Prism.languages.insertBefore("less", "punctuation", {
    "function": Prism.languages.less.function
});
Prism.languages.insertBefore("less", "property", {
    variable: [{
        pattern: /@[\w-]+\s*:/,
        inside: {
            punctuation: /:/
        }
    }, /@@?[\w-]+/],
    "mixin-usage": {
        pattern: /([{;]\s*)[.#](?!\d)[\w-]+.*?(?=[(;])/,
        lookbehind: !0,
        alias: "function"
    }
});
Prism.languages.markdown = Prism.languages.extend("markup", {});
Prism.languages.insertBefore("markdown", "prolog", {
    blockquote: {
        pattern: /^>(?:[\t ]*>)*/m,
        alias: "punctuation"
    },
    code: [{
        pattern: /^(?: {4}|\t).+/m,
        alias: "keyword"
    }, {
        pattern: /``.+?``|`[^`\n]+`/,
        alias: "keyword"
    }],
    title: [{
        pattern: /\w+.*(?:\r?\n|\r)(?:==+|--+)/,
        alias: "important",
        inside: {
            punctuation: /==+$|--+$/
        }
    }, {
        pattern: /(^\s*)#+.+/m,
        lookbehind: !0,
        alias: "important",
        inside: {
            punctuation: /^#+|#+$/
        }
    }],
    hr: {
        pattern: /(^\s*)([*-])(?:[\t ]*\2){2,}(?=\s*$)/m,
        lookbehind: !0,
        alias: "punctuation"
    },
    list: {
        pattern: /(^\s*)(?:[*+-]|\d+\.)(?=[\t ].)/m,
        lookbehind: !0,
        alias: "punctuation"
    },
    "url-reference": {
        pattern: /!?\[[^\]]+\]:[\t ]+(?:\S+|<(?:\\.|[^>\\])+>)(?:[\t ]+(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\)))?/,
        inside: {
            variable: {
                pattern: /^(!?\[)[^\]]+/,
                lookbehind: !0
            },
            string: /(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\))$/,
            punctuation: /^[\[\]!:]|[<>]/
        },
        alias: "url"
    },
    bold: {
        pattern: /(^|[^\\])(\*\*|__)(?:(?:\r?\n|\r)(?!\r?\n|\r)|.)+?\2/,
        lookbehind: !0,
        inside: {
            punctuation: /^\*\*|^__|\*\*$|__$/
        }
    },
    italic: {
        pattern: /(^|[^\\])([*_])(?:(?:\r?\n|\r)(?!\r?\n|\r)|.)+?\2/,
        lookbehind: !0,
        inside: {
            punctuation: /^[*_]|[*_]$/
        }
    },
    url: {
        pattern: /!?\[[^\]]+\](?:\([^\s)]+(?:[\t ]+"(?:\\.|[^"\\])*")?\)| ?\[[^\]\n]*\])/,
        inside: {
            variable: {
                pattern: /(!?\[)[^\]]+(?=\]$)/,
                lookbehind: !0
            },
            string: {
                pattern: /"(?:\\.|[^"\\])*"(?=\)$)/
            }
        }
    }
});
Prism.languages.markdown.bold.inside.url = Prism.languages.markdown.url;
Prism.languages.markdown.italic.inside.url = Prism.languages.markdown.url;
Prism.languages.markdown.bold.inside.italic = Prism.languages.markdown.italic;
Prism.languages.markdown.italic.inside.bold = Prism.languages.markdown.bold;
Prism.languages.nginx = Prism.languages.extend("clike", {
    comment: {
        pattern: /(^|[^"{\\])#.*/,
        lookbehind: !0
    },
    keyword: /\b(?:CONTENT_|DOCUMENT_|GATEWAY_|HTTP_|HTTPS|if_not_empty|PATH_|QUERY_|REDIRECT_|REMOTE_|REQUEST_|SCGI|SCRIPT_|SERVER_|http|events|accept_mutex|accept_mutex_delay|access_log|add_after_body|add_before_body|add_header|addition_types|aio|alias|allow|ancient_browser|ancient_browser_value|auth|auth_basic|auth_basic_user_file|auth_http|auth_http_header|auth_http_timeout|autoindex|autoindex_exact_size|autoindex_localtime|break|charset|charset_map|charset_types|chunked_transfer_encoding|client_body_buffer_size|client_body_in_file_only|client_body_in_single_buffer|client_body_temp_path|client_body_timeout|client_header_buffer_size|client_header_timeout|client_max_body_size|connection_pool_size|create_full_put_path|daemon|dav_access|dav_methods|debug_connection|debug_points|default_type|deny|devpoll_changes|devpoll_events|directio|directio_alignment|disable_symlinks|empty_gif|env|epoll_events|error_log|error_page|expires|fastcgi_buffer_size|fastcgi_buffers|fastcgi_busy_buffers_size|fastcgi_cache|fastcgi_cache_bypass|fastcgi_cache_key|fastcgi_cache_lock|fastcgi_cache_lock_timeout|fastcgi_cache_methods|fastcgi_cache_min_uses|fastcgi_cache_path|fastcgi_cache_purge|fastcgi_cache_use_stale|fastcgi_cache_valid|fastcgi_connect_timeout|fastcgi_hide_header|fastcgi_ignore_client_abort|fastcgi_ignore_headers|fastcgi_index|fastcgi_intercept_errors|fastcgi_keep_conn|fastcgi_max_temp_file_size|fastcgi_next_upstream|fastcgi_no_cache|fastcgi_param|fastcgi_pass|fastcgi_pass_header|fastcgi_read_timeout|fastcgi_redirect_errors|fastcgi_send_timeout|fastcgi_split_path_info|fastcgi_store|fastcgi_store_access|fastcgi_temp_file_write_size|fastcgi_temp_path|flv|geo|geoip_city|geoip_country|google_perftools_profiles|gzip|gzip_buffers|gzip_comp_level|gzip_disable|gzip_http_version|gzip_min_length|gzip_proxied|gzip_static|gzip_types|gzip_vary|if|if_modified_since|ignore_invalid_headers|image_filter|image_filter_buffer|image_filter_jpeg_quality|image_filter_sharpen|image_filter_transparency|imap_capabilities|imap_client_buffer|include|index|internal|ip_hash|keepalive|keepalive_disable|keepalive_requests|keepalive_timeout|kqueue_changes|kqueue_events|large_client_header_buffers|limit_conn|limit_conn_log_level|limit_conn_zone|limit_except|limit_rate|limit_rate_after|limit_req|limit_req_log_level|limit_req_zone|limit_zone|lingering_close|lingering_time|lingering_timeout|listen|location|lock_file|log_format|log_format_combined|log_not_found|log_subrequest|map|map_hash_bucket_size|map_hash_max_size|master_process|max_ranges|memcached_buffer_size|memcached_connect_timeout|memcached_next_upstream|memcached_pass|memcached_read_timeout|memcached_send_timeout|merge_slashes|min_delete_depth|modern_browser|modern_browser_value|mp4|mp4_buffer_size|mp4_max_buffer_size|msie_padding|msie_refresh|multi_accept|open_file_cache|open_file_cache_errors|open_file_cache_min_uses|open_file_cache_valid|open_log_file_cache|optimize_server_names|override_charset|pcre_jit|perl|perl_modules|perl_require|perl_set|pid|pop3_auth|pop3_capabilities|port_in_redirect|post_action|postpone_output|protocol|proxy|proxy_buffer|proxy_buffer_size|proxy_buffering|proxy_buffers|proxy_busy_buffers_size|proxy_cache|proxy_cache_bypass|proxy_cache_key|proxy_cache_lock|proxy_cache_lock_timeout|proxy_cache_methods|proxy_cache_min_uses|proxy_cache_path|proxy_cache_use_stale|proxy_cache_valid|proxy_connect_timeout|proxy_cookie_domain|proxy_cookie_path|proxy_headers_hash_bucket_size|proxy_headers_hash_max_size|proxy_hide_header|proxy_http_version|proxy_ignore_client_abort|proxy_ignore_headers|proxy_intercept_errors|proxy_max_temp_file_size|proxy_method|proxy_next_upstream|proxy_no_cache|proxy_pass|proxy_pass_error_message|proxy_pass_header|proxy_pass_request_body|proxy_pass_request_headers|proxy_read_timeout|proxy_redirect|proxy_redirect_errors|proxy_send_lowat|proxy_send_timeout|proxy_set_body|proxy_set_header|proxy_ssl_session_reuse|proxy_store|proxy_store_access|proxy_temp_file_write_size|proxy_temp_path|proxy_timeout|proxy_upstream_fail_timeout|proxy_upstream_max_fails|random_index|read_ahead|real_ip_header|recursive_error_pages|request_pool_size|reset_timedout_connection|resolver|resolver_timeout|return|rewrite|root|rtsig_overflow_events|rtsig_overflow_test|rtsig_overflow_threshold|rtsig_signo|satisfy|satisfy_any|secure_link_secret|send_lowat|send_timeout|sendfile|sendfile_max_chunk|server|server_name|server_name_in_redirect|server_names_hash_bucket_size|server_names_hash_max_size|server_tokens|set|set_real_ip_from|smtp_auth|smtp_capabilities|so_keepalive|source_charset|split_clients|ssi|ssi_silent_errors|ssi_types|ssi_value_length|ssl|ssl_certificate|ssl_certificate_key|ssl_ciphers|ssl_client_certificate|ssl_crl|ssl_dhparam|ssl_engine|ssl_prefer_server_ciphers|ssl_protocols|ssl_session_cache|ssl_session_timeout|ssl_verify_client|ssl_verify_depth|starttls|stub_status|sub_filter|sub_filter_once|sub_filter_types|tcp_nodelay|tcp_nopush|timeout|timer_resolution|try_files|types|types_hash_bucket_size|types_hash_max_size|underscores_in_headers|uninitialized_variable_warn|upstream|use|user|userid|userid_domain|userid_expires|userid_name|userid_p3p|userid_path|userid_service|valid_referers|variables_hash_bucket_size|variables_hash_max_size|worker_connections|worker_cpu_affinity|worker_priority|worker_processes|worker_rlimit_core|worker_rlimit_nofile|worker_rlimit_sigpending|working_directory|xclient|xml_entities|xslt_entities|xslt_stylesheet|xslt_types)\b/i
});
Prism.languages.insertBefore("nginx", "keyword", {
    variable: /\$[a-z_]+/i
});
(function (b) {
    b.languages.php = b.languages.extend("clike", {
        keyword: /\b(?:and|or|xor|array|as|break|case|cfunction|class|const|continue|declare|default|die|do|else|elseif|enddeclare|endfor|endforeach|endif|endswitch|endwhile|extends|for|foreach|function|include|include_once|global|if|new|return|static|switch|use|require|require_once|var|while|abstract|interface|public|implements|private|protected|parent|throw|null|echo|print|trait|namespace|final|yield|goto|instanceof|finally|try|catch)\b/i,
        constant: /\b[A-Z0-9_]{2,}\b/,
        comment: {
            pattern: /(^|[^\\])(?:\/\*[\s\S]*?\*\/|\/\/.*)/,
            lookbehind: !0
        }
    });
    b.languages.insertBefore("php", "string", {
        "shell-comment": {
            pattern: /(^|[^\\])#.*/,
            lookbehind: !0,
            alias: "comment"
        }
    });
    b.languages.insertBefore("php", "keyword", {
        delimiter: {
            pattern: /\?>|<\?(?:php|=)?/i,
            alias: "important"
        },
        variable: /\$+(?:\w+\b|(?={))/i,
        "package": {
            pattern: /(\\|namespace\s+|use\s+)[\w\\]+/,
            lookbehind: !0,
            inside: {
                punctuation: /\\/
            }
        }
    });
    b.languages.insertBefore("php", "operator", {
        property: {
            pattern: /(->)[\w]+/,
            lookbehind: !0
        }
    });
    b.languages.insertBefore("php", "string", {
        "nowdoc-string": {
            pattern: /<<<'([^']+)'(?:\r\n?|\n)(?:.*(?:\r\n?|\n))*?\1;/,
            greedy: !0,
            alias: "string",
            inside: {
                delimiter: {
                    pattern: /^<<<'[^']+'|[a-z_]\w*;$/i,
                    alias: "symbol",
                    inside: {
                        punctuation: /^<<<'?|[';]$/
                    }
                }
            }
        },
        "heredoc-string": {
            pattern: /<<<(?:"([^"]+)"(?:\r\n?|\n)(?:.*(?:\r\n?|\n))*?\1;|([a-z_]\w*)(?:\r\n?|\n)(?:.*(?:\r\n?|\n))*?\2;)/i,
            greedy: !0,
            alias: "string",
            inside: {
                delimiter: {
                    pattern: /^<<<(?:"[^"]+"|[a-z_]\w*)|[a-z_]\w*;$/i,
                    alias: "symbol",
                    inside: {
                        punctuation: /^<<<"?|[";]$/
                    }
                },
                interpolation: null
            }
        },
        "single-quoted-string": {
            pattern: /'(?:\\[\s\S]|[^\\'])*'/,
            greedy: !0,
            alias: "string"
        },
        "double-quoted-string": {
            pattern: /"(?:\\[\s\S]|[^\\"])*"/,
            greedy: !0,
            alias: "string",
            inside: {
                interpolation: null
            }
        }
    });
    delete b.languages.php.string;
    var e = {
        pattern: /{\$(?:{(?:{[^{}]+}|[^{}]+)}|[^{}])+}|(^|[^\\{])\$+(?:\w+(?:\[.+?]|->\w+)*)/,
        lookbehind: !0,
        inside: {
            rest: b.languages.php
        }
    };
    b.languages.php["heredoc-string"].inside.interpolation = e;
    b.languages.php["double-quoted-string"].inside.interpolation =
        e;
    b.hooks.add("before-tokenize", function (c) {
        /(?:<\?php|<\?)/ig.test(c.code) && b.languages["markup-templating"].buildPlaceholders(c, "php", /(?:<\?php|<\?)[\s\S]*?(?:\?>|$)/ig)
    });
    b.hooks.add("after-tokenize", function (c) {
        b.languages["markup-templating"].tokenizePlaceholders(c, "php")
    })
})(Prism);
Prism.languages.sql = {
    comment: {
        pattern: /(^|[^\\])(?:\/\*[\s\S]*?\*\/|(?:--|\/\/|#).*)/,
        lookbehind: !0
    },
    string: {
        pattern: /(^|[^@\\])("|')(?:\\[\s\S]|(?!\2)[^\\])*\2/,
        greedy: !0,
        lookbehind: !0
    },
    variable: /@[\w.$]+|@(["'`])(?:\\[\s\S]|(?!\1)[^\\])+\1/,
    "function": /\b(?:AVG|COUNT|FIRST|FORMAT|LAST|LCASE|LEN|MAX|MID|MIN|MOD|NOW|ROUND|SUM|UCASE)(?=\s*\()/i,
    keyword: /\b(?:ACTION|ADD|AFTER|ALGORITHM|ALL|ALTER|ANALYZE|ANY|APPLY|AS|ASC|AUTHORIZATION|AUTO_INCREMENT|BACKUP|BDB|BEGIN|BERKELEYDB|BIGINT|BINARY|BIT|BLOB|BOOL|BOOLEAN|BREAK|BROWSE|BTREE|BULK|BY|CALL|CASCADED?|CASE|CHAIN|CHAR(?:ACTER|SET)?|CHECK(?:POINT)?|CLOSE|CLUSTERED|COALESCE|COLLATE|COLUMNS?|COMMENT|COMMIT(?:TED)?|COMPUTE|CONNECT|CONSISTENT|CONSTRAINT|CONTAINS(?:TABLE)?|CONTINUE|CONVERT|CREATE|CROSS|CURRENT(?:_DATE|_TIME|_TIMESTAMP|_USER)?|CURSOR|CYCLE|DATA(?:BASES?)?|DATE(?:TIME)?|DAY|DBCC|DEALLOCATE|DEC|DECIMAL|DECLARE|DEFAULT|DEFINER|DELAYED|DELETE|DELIMITERS?|DENY|DESC|DESCRIBE|DETERMINISTIC|DISABLE|DISCARD|DISK|DISTINCT|DISTINCTROW|DISTRIBUTED|DO|DOUBLE|DROP|DUMMY|DUMP(?:FILE)?|DUPLICATE|ELSE(?:IF)?|ENABLE|ENCLOSED|END|ENGINE|ENUM|ERRLVL|ERRORS|ESCAPED?|EXCEPT|EXEC(?:UTE)?|EXISTS|EXIT|EXPLAIN|EXTENDED|FETCH|FIELDS|FILE|FILLFACTOR|FIRST|FIXED|FLOAT|FOLLOWING|FOR(?: EACH ROW)?|FORCE|FOREIGN|FREETEXT(?:TABLE)?|FROM|FULL|FUNCTION|GEOMETRY(?:COLLECTION)?|GLOBAL|GOTO|GRANT|GROUP|HANDLER|HASH|HAVING|HOLDLOCK|HOUR|IDENTITY(?:_INSERT|COL)?|IF|IGNORE|IMPORT|INDEX|INFILE|INNER|INNODB|INOUT|INSERT|INT|INTEGER|INTERSECT|INTERVAL|INTO|INVOKER|ISOLATION|ITERATE|JOIN|KEYS?|KILL|LANGUAGE|LAST|LEAVE|LEFT|LEVEL|LIMIT|LINENO|LINES|LINESTRING|LOAD|LOCAL|LOCK|LONG(?:BLOB|TEXT)|LOOP|MATCH(?:ED)?|MEDIUM(?:BLOB|INT|TEXT)|MERGE|MIDDLEINT|MINUTE|MODE|MODIFIES|MODIFY|MONTH|MULTI(?:LINESTRING|POINT|POLYGON)|NATIONAL|NATURAL|NCHAR|NEXT|NO|NONCLUSTERED|NULLIF|NUMERIC|OFF?|OFFSETS?|ON|OPEN(?:DATASOURCE|QUERY|ROWSET)?|OPTIMIZE|OPTION(?:ALLY)?|ORDER|OUT(?:ER|FILE)?|OVER|PARTIAL|PARTITION|PERCENT|PIVOT|PLAN|POINT|POLYGON|PRECEDING|PRECISION|PREPARE|PREV|PRIMARY|PRINT|PRIVILEGES|PROC(?:EDURE)?|PUBLIC|PURGE|QUICK|RAISERROR|READS?|REAL|RECONFIGURE|REFERENCES|RELEASE|RENAME|REPEAT(?:ABLE)?|REPLACE|REPLICATION|REQUIRE|RESIGNAL|RESTORE|RESTRICT|RETURNS?|REVOKE|RIGHT|ROLLBACK|ROUTINE|ROW(?:COUNT|GUIDCOL|S)?|RTREE|RULE|SAVE(?:POINT)?|SCHEMA|SECOND|SELECT|SERIAL(?:IZABLE)?|SESSION(?:_USER)?|SET(?:USER)?|SHARE|SHOW|SHUTDOWN|SIMPLE|SMALLINT|SNAPSHOT|SOME|SONAME|SQL|START(?:ING)?|STATISTICS|STATUS|STRIPED|SYSTEM_USER|TABLES?|TABLESPACE|TEMP(?:ORARY|TABLE)?|TERMINATED|TEXT(?:SIZE)?|THEN|TIME(?:STAMP)?|TINY(?:BLOB|INT|TEXT)|TOP?|TRAN(?:SACTIONS?)?|TRIGGER|TRUNCATE|TSEQUAL|TYPES?|UNBOUNDED|UNCOMMITTED|UNDEFINED|UNION|UNIQUE|UNLOCK|UNPIVOT|UNSIGNED|UPDATE(?:TEXT)?|USAGE|USE|USER|USING|VALUES?|VAR(?:BINARY|CHAR|CHARACTER|YING)|VIEW|WAITFOR|WARNINGS|WHEN|WHERE|WHILE|WITH(?: ROLLUP|IN)?|WORK|WRITE(?:TEXT)?|YEAR)\b/i,
    "boolean": /\b(?:TRUE|FALSE|NULL)\b/i,
    number: /\b0x[\da-f]+\b|\b\d+\.?\d*|\B\.\d+\b/i,
    operator: /[-+*\/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?|\b(?:AND|BETWEEN|IN|LIKE|NOT|OR|IS|DIV|REGEXP|RLIKE|SOUNDS LIKE|XOR)\b/i,
    punctuation: /[;[\]()`,.]/
};
Prism.languages.python = {
    comment: {
        pattern: /(^|[^\\])#.*/,
        lookbehind: !0
    },
    "triple-quoted-string": {
        pattern: /("""|''')[\s\S]+?\1/,
        greedy: !0,
        alias: "string"
    },
    string: {
        pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/,
        greedy: !0
    },
    "function": {
        pattern: /((?:^|\s)def[ \t]+)[a-zA-Z_]\w*(?=\s*\()/g,
        lookbehind: !0
    },
    "class-name": {
        pattern: /(\bclass\s+)\w+/i,
        lookbehind: !0
    },
    keyword: /\b(?:as|assert|async|await|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|nonlocal|pass|print|raise|return|try|while|with|yield|self)\b/,
    module: /\b(?:exceptions|os|os.path|stat|string|re|math|cmath|operator|copy|sys|atexit|time|datetime|types|gc|io|functools|codecs|json|thread|threading|hashlib|shutil|md5|code|random)\b/,
    builtin: /\b(?:__import__|abs|all|any|apply|ascii|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip|isfile|mkdir|makedirs|exists|strftime)\b/,
    "boolean": /\b(?:True|False|None)\b/,
    number: /(?:\b(?=\d)|\B(?=\.))(?:0[bo])?(?:(?:\d|0x[\da-f])[\da-f]*\.?\d*|\.\d+)(?:e[+-]?\d+)?j?\b/i,
    operator: /[-+%=]=?|!=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]|\b(?:or|and|not)\b/,
    punctuation: /[{}[\];(),.:]/
};
(function (b) {
    b.languages.smarty = {
        comment: /\{\*[\s\S]*?\*\}/,
        delimiter: {
            pattern: /^\{|\}$/i,
            alias: "punctuation"
        },
        string: /(["'])(?:\\.|(?!\1)[^\\\r\n])*\1/,
        number: /\b0x[\dA-Fa-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee][-+]?\d+)?/,
        variable: [/\$(?!\d)\w+/, /#(?!\d)\w+#/, {
            pattern: /(\.|->)(?!\d)\w+/,
            lookbehind: !0
        }, {
            pattern: /(\[)(?!\d)\w+(?=\])/,
            lookbehind: !0
        }],
        "function": [{
            pattern: /(\|\s*)@?(?!\d)\w+/,
            lookbehind: !0
        }, /^\/?(?!\d)\w+/, /(?!\d)\w+(?=\()/],
        "attr-name": {
            pattern: /\w+\s*=\s*(?:(?!\d)\w+)?/,
            inside: {
                variable: {
                    pattern: /(=\s*)(?!\d)\w+/,
                    lookbehind: !0
                },
                operator: /=/
            }
        },
        punctuation: [/[\[\]().,:`]|->/],
        operator: [/[+\-*\/%]|==?=?|[!<>]=?|&&|\|\|?/, /\bis\s+(?:not\s+)?(?:div|even|odd)(?:\s+by)?\b/, /\b(?:eq|neq?|gt|lt|gt?e|lt?e|not|mod|or|and)\b/],
        keyword: /\b(?:false|off|on|no|true|yes)\b/
    };
    b.languages.insertBefore("smarty", "tag", {
        "smarty-comment": {
            pattern: /\{\*[\s\S]*?\*\}/,
            alias: ["smarty", "comment"]
        }
    });
    b.hooks.add("before-tokenize", function (e) {
        var c = !1;
        b.languages["markup-templating"].buildPlaceholders(e, "smarty", /\{\*[\s\S]*?\*\}|\{[\s\S]+?\}/g,
            function (b) {
                "{/literal}" === b && (c = !1);
                return c ? !1 : ("{literal}" === b && (c = !0), !0)
            })
    });
    b.hooks.add("after-tokenize", function (e) {
        b.languages["markup-templating"].tokenizePlaceholders(e, "smarty")
    })
})(Prism);
(function () {
    if ("undefined" !== typeof self && self.Prism && self.document) {
        var b = /\n(?!$)/g,
            e = function (d) {
                var e = c(d)["white-space"];
                if ("pre-wrap" === e || "pre-line" === e) {
                    e = d.querySelector("pre");
                    var a = d.querySelector(".line-numbers-rows"),
                        f = d.querySelector(".line-numbers-sizer");
                    d = e.textContent.split(b);
                    f || (f = document.createElement("div"), f.className = "line-numbers-sizer", e.appendChild(f));
                    f.style.display = "block";
                    d.forEach(function (b, c) {
                        f.textContent = b || "\n";
                        b = f.getBoundingClientRect().height;
                        a.children[c].style.height =
                            b + "px"
                    });
                    f.textContent = "";
                    f.style.display = "none"
                }
            },
            c = function (b) {
                return b ? window.getComputedStyle ? getComputedStyle(b) : b.currentStyle || null : null
            };
        window.addEventListener("resize", function () {
            Array.prototype.forEach.call(document.querySelectorAll("pre.line-numbers"), e)
        });
        Prism.hooks.add("complete", function (c) {
            if (c.code) {
                var d = c.element.parentNode,
                    a = /\s*\bline-numbers\b\s*/;
                if (d && /pre/i.test(d.nodeName) && (a.test(d.className) || a.test(c.element.className)) && !c.element.querySelector(".line-numbers-rows")) {
                    a.test(c.element.className) &&
                        (c.element.className = c.element.className.replace(a, " "));
                    a.test(d.className) || (d.className += " line-numbers");
                    a = c.code.match(b);
                    var f = Array((a ? a.length + 1 : 1) + 1);
                    f = f.join("<span></span>");
                    a = document.createElement("span");
                    a.setAttribute("aria-hidden", "true");
                    a.className = "line-numbers-rows";
                    a.innerHTML = f;
                    d.hasAttribute("data-start") && (d.style.counterReset = "linenumber " + (parseInt(d.getAttribute("data-start"), 10) - 1));
                    c.element.appendChild(a);
                    e(d);
                    Prism.hooks.run("line-numbers", c)
                }
            }
        });
        Prism.hooks.add("line-numbers",
            function (b) {
                b.plugins = b.plugins || {};
                b.plugins.lineNumbers = !0
            });
        Prism.plugins.lineNumbers = {
            getLine: function (b, c) {
                if ("PRE" === b.tagName && b.classList.contains("line-numbers")) {
                    var a = b.querySelector(".line-numbers-rows");
                    b = parseInt(b.getAttribute("data-start"), 10) || 1;
                    var f = b + (a.children.length - 1);
                    c < b && (c = b);
                    c > f && (c = f);
                    return a.children[c - b]
                }
            }
        }
    }
})();
(function () {
    if ("undefined" !== typeof self && self.Prism && self.document) {
        var b = [],
            e = {},
            c = function () {};
        Prism.plugins.toolbar = {};
        var d = Prism.plugins.toolbar.registerButton = function (a, c) {
                b.push(e[a] = "function" === typeof c ? c : function (b) {
                    if ("function" === typeof c.onClick) {
                        var a = document.createElement("button");
                        a.type = "button";
                        a.addEventListener("click", function () {
                            c.onClick.call(this, b)
                        })
                    } else "string" === typeof c.url ? (a = document.createElement("a"), a.href = c.url) : a = document.createElement("span");
                    a.textContent = c.text;
                    return a
                })
            },
            k = Prism.plugins.toolbar.hook = function (a) {
                var d = a.element.parentNode;
                if (d && /pre/i.test(d.nodeName) && !d.parentNode.classList.contains("code-toolbar")) {
                    var g = document.createElement("div");
                    g.classList.add("code-toolbar");
                    d.parentNode.insertBefore(g, d);
                    g.appendChild(d);
                    d = document.createElement("div");
                    d.classList.add("shelter");
                    g.appendChild(d);
                    var k = document.createElement("div");
                    k.classList.add("toolbar");
                    document.body.hasAttribute("data-toolbar-order") && (b = document.body.getAttribute("data-toolbar-order").split(",").map(function (a) {
                        return e[a] ||
                            c
                    }));
                    b.forEach(function (b) {
                        if (b = b(a)) {
                            var c = document.createElement("div");
                            c.classList.add("toolbar-item");
                            c.appendChild(b);
                            k.appendChild(c)
                        }
                    });
                    g.appendChild(k)
                }
            };
        d("label", function (a) {
            if ((a = a.element.parentNode) && /pre/i.test(a.nodeName) && a.hasAttribute("data-label")) {
                var b = a.getAttribute("data-label");
                try {
                    var c = document.querySelector("template#" + b)
                } catch (l) {}
                c ? c = c.content : (a.hasAttribute("data-url") ? (c = document.createElement("a"), c.href = a.getAttribute("data-url")) : c = document.createElement("span"),
                    c.textContent = b);
                return c
            }
        });
        Prism.hooks.add("complete", k)
    }
})();
(function () {
    if ("undefined" !== typeof self && self.Prism && self.document)
        if (Prism.plugins.toolbar) {
            var b = {
                html: "HTML",
                xml: "XML",
                svg: "SVG",
                mathml: "MathML",
                css: "CSS",
                clike: "C-like",
                javascript: "JavaScript",
                abap: "ABAP",
                actionscript: "ActionScript",
                apacheconf: "Apache Configuration",
                apl: "APL",
                applescript: "AppleScript",
                arff: "ARFF",
                asciidoc: "AsciiDoc",
                asm6502: "6502 Assembly",
                aspnet: "ASP.NET (C#)",
                autohotkey: "AutoHotkey",
                autoit: "AutoIt",
                basic: "BASIC",
                csharp: "C#",
                cpp: "C++",
                coffeescript: "CoffeeScript",
                csp: "Content-Security-Policy",
                "css-extras": "CSS Extras",
                django: "Django/Jinja2",
                erb: "ERB",
                fsharp: "F#",
                gedcom: "GEDCOM",
                glsl: "GLSL",
                graphql: "GraphQL",
                http: "HTTP",
                hpkp: "HTTP Public-Key-Pins",
                hsts: "HTTP Strict-Transport-Security",
                ichigojam: "IchigoJam",
                inform7: "Inform 7",
                json: "JSON",
                latex: "LaTeX",
                livescript: "LiveScript",
                lolcode: "LOLCODE",
                "markup-templating": "Markup templating",
                matlab: "MATLAB",
                mel: "MEL",
                n4js: "N4JS",
                nasm: "NASM",
                nginx: "nginx",
                nsis: "NSIS",
                objectivec: "Objective-C",
                ocaml: "OCaml",
                opencl: "OpenCL",
                parigp: "PARI/GP",
                php: "PHP",
                "php-extras": "PHP Extras",
                plsql: "PL/SQL",
                powershell: "PowerShell",
                properties: ".properties",
                protobuf: "Protocol Buffers",
                q: "Q (kdb+ database)",
                jsx: "React JSX",
                tsx: "React TSX",
                renpy: "Ren'py",
                rest: "reST (reStructuredText)",
                sas: "SAS",
                sass: "Sass (Sass)",
                scss: "Sass (Scss)",
                sql: "SQL",
                go: "GO",
                soy: "Soy (Closure Template)",
                typescript: "TypeScript",
                vbnet: "VB.Net",
                vhdl: "VHDL",
                vim: "vim",
                "visual-basic": "Visual Basic",
                wasm: "WebAssembly",
                wiki: "Wiki markup",
                xojo: "Xojo (REALbasic)",
                yaml: "YAML"
            };
            Prism.plugins.toolbar.registerButton("show-language",
                function (e) {
                    var c = e.element.parentNode;
                    if (c && /pre/i.test(c.nodeName) && (e = c.getAttribute("data-language") || b[e.language] || e.language && e.language.substring(0, 1).toUpperCase() + e.language.substring(1))) return c = document.createElement("span"), c.textContent = e, c
                })
        } else console.warn("Show Languages plugin loaded before Toolbar plugin.")
})();
Prism.languages.clike = {
    comment: [{
        pattern: /(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/,
        lookbehind: !0
    }, {
        pattern: /(^|[^\\:])\/\/.*/,
        lookbehind: !0,
        greedy: !0
    }],
    string: {
        pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
        greedy: !0
    },
    "class-name": {
        pattern: /(\b(?:class|interface|extends|implements|trait|instanceof|new)\s+|\bcatch\s+\()[\w.\\]+/i,
        lookbehind: !0,
        inside: {
            punctuation: /[.\\]/
        }
    },
    keyword: /\b(?:if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue)\b/,
    boolean: /\b(?:true|false)\b/,
    function: /\w+(?=\()/,
    number: /\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?/i,
    operator: /[<>]=?|[!=]=?=?|--?|\+\+?|&&?|\|\|?|[?*/~^%]/,
    punctuation: /[{}[\];(),.:]/
};
Prism.languages.go = Prism.languages.extend("clike", {
    keyword: /\b(?:break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go(?:to)?|if|import|interface|map|package|range|return|select|struct|switch|type|var)\b/,
    builtin: /\b(?:bool|byte|complex(?:64|128)|error|float(?:32|64)|rune|string|u?int(?:8|16|32|64)?|uintptr|append|cap|close|complex|copy|delete|imag|len|make|new|panic|print(?:ln)?|real|recover)\b/,
    boolean: /\b(?:_|iota|nil|true|false)\b/,
    operator: /[*\/%^!=]=?|\+[=+]?|-[=-]?|\|[=|]?|&(?:=|&|\^=?)?|>(?:>=?|=)?|<(?:<=?|=|-)?|:=|\.\.\./,
    number: /(?:\b0x[a-f\d]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[-+]?\d+)?)i?/i,
    string: {
        pattern: /(["'`])(?:\\[\s\S]|(?!\1)[^\\])*\1/,
        greedy: !0
    }
});
delete Prism.languages.go["class-name"];
(function () {
    if ("undefined" !== typeof self && self.Prism && self.document)
        if (Prism.plugins.toolbar) {
            var b = window.ClipboardJS || void 0;
            b || "function" !== typeof require || (b = require("clipboard"));
            var e = [];
            if (!b) {
                var c = document.createElement("script"),
                    d = document.querySelector("head");
                c.onload = function () {
                    if (b = window.ClipboardJS)
                        for (; e.length;) e.pop()()
                };
                c.src = "https://cdn.jsdelivr.net/npm/clipboard@2.0.6/dist/clipboard.min.js";
                d.appendChild(c)
            }
            Prism.plugins.toolbar.registerButton("copy-to-clipboard", function (c) {
                function a() {
                    var a =
                        new b(g, {
                            text: function () {
                                return c.code
                            }
                        });
                    a.on("success", function () {
                        g.innerHTML = '<i class="fontello fontello-tags" id="btn-copy-code"style="font-style:normal;"> \u5df2\u590d\u5236</i>';
                        d()
                    });
                    a.on("error", function () {
                        g.textContent = "Press Ctrl+C to copy";
                        d()
                    })
                }

                function d() {
                    setTimeout(function () {
                        g.innerHTML = '<i class="fontello fontello-tags" id="btn-copy-code"style="font-style:normal;"> \u590d\u5236</i>'
                    }, 5E3)
                }
                var g = document.createElement("button");
                g.innerHTML = '<i class="fontello fontello-tags" id="btn-copy-code"style="font-style:normal;"> \u590d\u5236</i>';
                b ? a() : e.push(a);
                return g
            })
        } else console.warn("Copy to Clipboard plugin loaded before Toolbar plugin.")
})();