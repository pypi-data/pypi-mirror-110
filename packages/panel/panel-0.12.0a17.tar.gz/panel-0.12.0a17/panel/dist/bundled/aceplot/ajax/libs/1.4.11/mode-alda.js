define("ace/mode/alda_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],function(e,t,n){"use strict";var r=e("../lib/oop"),i=e("./text_highlight_rules").TextHighlightRules,s=function(){this.$rules={pitch:[{token:"variable.parameter.operator.pitch.alda",regex:/(?:[+\-]+|\=)/},{token:"",regex:"",next:"timing"}],timing:[{token:"string.quoted.operator.timing.alda",regex:/\d+(?:s|ms)?/},{token:"",regex:"",next:"start"}],start:[{token:["constant.language.instrument.alda","constant.language.instrument.alda","meta.part.call.alda","storage.type.nickname.alda","meta.part.call.alda"],regex:/^([a-zA-Z]{2}[\w\-+\'()]*)((?:\s*\/\s*[a-zA-Z]{2}[\w\-+\'()]*)*)(?:(\s*)(\"[a-zA-Z]{2}[\w\-+\'()]*\"))?(\s*:)/},{token:["text","entity.other.inherited-class.voice.alda","text"],regex:/^(\s*)(V\d+)(:)/},{token:"comment.line.number-sign.alda",regex:/#.*$/},{token:"entity.name.function.pipe.measure.alda",regex:/\|/},{token:"comment.block.inline.alda",regex:/\(comment\b/,push:[{token:"comment.block.inline.alda",regex:/\)/,next:"pop"},{defaultToken:"comment.block.inline.alda"}]},{token:"entity.name.function.marker.alda",regex:/%[a-zA-Z]{2}[\w\-+\'()]*/},{token:"entity.name.function.at-marker.alda",regex:/@[a-zA-Z]{2}[\w\-+\'()]*/},{token:"keyword.operator.octave-change.alda",regex:/\bo\d+\b/},{token:"keyword.operator.octave-shift.alda",regex:/[><]/},{token:"keyword.operator.repeat.alda",regex:/\*\s*\d+/},{token:"string.quoted.operator.timing.alda",regex:/[.]|r\d*(?:s|ms)?/},{token:"text",regex:/([cdefgab])/,next:"pitch"},{token:"string.quoted.operator.timing.alda",regex:/~/,next:"timing"},{token:"punctuation.section.embedded.cram.alda",regex:/\}/,next:"timing"},{token:"constant.numeric.subchord.alda",regex:/\//},{todo:{token:"punctuation.section.embedded.cram.alda",regex:/\{/,push:[{token:"punctuation.section.embedded.cram.alda",regex:/\}/,next:"pop"},{include:"$self"}]}},{todo:{token:"keyword.control.sequence.alda",regex:/\[/,push:[{token:"keyword.control.sequence.alda",regex:/\]/,next:"pop"},{include:"$self"}]}},{token:"meta.inline.clojure.alda",regex:/\(/,push:[{token:"meta.inline.clojure.alda",regex:/\)/,next:"pop"},{include:"source.clojure"},{defaultToken:"meta.inline.clojure.alda"}]}]},this.normalizeRules()};s.metaData={scopeName:"source.alda",fileTypes:["alda"],name:"Alda"},r.inherits(s,i),t.AldaHighlightRules=s}),define("ace/mode/folding/cstyle",["require","exports","module","ace/lib/oop","ace/range","ace/mode/folding/fold_mode"],function(e,t,n){"use strict";var r=e("../../lib/oop"),i=e("../../range").Range,s=e("./fold_mode").FoldMode,o=t.FoldMode=function(e){e&&(this.foldingStartMarker=new RegExp(this.foldingStartMarker.source.replace(/\|[^|]*?$/,"|"+e.start)),this.foldingStopMarker=new RegExp(this.foldingStopMarker.source.replace(/\|[^|]*?$/,"|"+e.end)))};r.inherits(o,s),function(){this.foldingStartMarker=/([\{\[\(])[^\}\]\)]*$|^\s*(\/\*)/,this.foldingStopMarker=/^[^\[\{\(]*([\}\]\)])|^[\s\*]*(\*\/)/,this.singleLineBlockCommentRe=/^\s*(\/\*).*\*\/\s*$/,this.tripleStarBlockCommentRe=/^\s*(\/\*\*\*).*\*\/\s*$/,this.startRegionRe=/^\s*(\/\*|\/\/)#?region\b/,this._getFoldWidgetBase=this.getFoldWidget,this.getFoldWidget=function(e,t,n){var r=e.getLine(n);if(this.singleLineBlockCommentRe.test(r)&&!this.startRegionRe.test(r)&&!this.tripleStarBlockCommentRe.test(r))return"";var i=this._getFoldWidgetBase(e,t,n);return!i&&this.startRegionRe.test(r)?"start":i},this.getFoldWidgetRange=function(e,t,n,r){var i=e.getLine(n);if(this.startRegionRe.test(i))return this.getCommentRegionBlock(e,i,n);var s=i.match(this.foldingStartMarker);if(s){var o=s.index;if(s[1])return this.openingBracketBlock(e,s[1],n,o);var u=e.getCommentFoldRange(n,o+s[0].length,1);return u&&!u.isMultiLine()&&(r?u=this.getSectionRange(e,n):t!="all"&&(u=null)),u}if(t==="markbegin")return;var s=i.match(this.foldingStopMarker);if(s){var o=s.index+s[0].length;return s[1]?this.closingBracketBlock(e,s[1],n,o):e.getCommentFoldRange(n,o,-1)}},this.getSectionRange=function(e,t){var n=e.getLine(t),r=n.search(/\S/),s=t,o=n.length;t+=1;var u=t,a=e.getLength();while(++t<a){n=e.getLine(t);var f=n.search(/\S/);if(f===-1)continue;if(r>f)break;var l=this.getFoldWidgetRange(e,"all",t);if(l){if(l.start.row<=s)break;if(l.isMultiLine())t=l.end.row;else if(r==f)break}u=t}return new i(s,o,u,e.getLine(u).length)},this.getCommentRegionBlock=function(e,t,n){var r=t.search(/\s*$/),s=e.getLength(),o=n,u=/^\s*(?:\/\*|\/\/|--)#?(end)?region\b/,a=1;while(++n<s){t=e.getLine(n);var f=u.exec(t);if(!f)continue;f[1]?a--:a++;if(!a)break}var l=n;if(l>o)return new i(o,r,l,t.length)}}.call(o.prototype)}),define("ace/mode/alda",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/alda_highlight_rules","ace/mode/folding/cstyle"],function(e,t,n){"use strict";var r=e("../lib/oop"),i=e("./text").Mode,s=e("./alda_highlight_rules").AldaHighlightRules,o=e("./folding/cstyle").FoldMode,u=function(){this.HighlightRules=s,this.foldingRules=new o};r.inherits(u,i),function(){this.$id="ace/mode/alda"}.call(u.prototype),t.Mode=u});                (function() {
                    window.require(["ace/mode/alda"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            