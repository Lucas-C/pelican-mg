A patch was applied to [lazysizes](https://github.com/aFarkas/lazysizes) plugin,
in [ls.noscript.js](https://github.com/aFarkas/lazysizes/blob/4.0.0-rc3/plugins/noscript/ls.noscript.js),
in order to prepend the `.lazyloaded <img>` into the target container,
in order to preserve `<figcaption>` in such case:

```html
<figure class="lazyload" data-noscript="">
  <noscript><img ...></noscript>
  <figcaption>...</figcaption>
</figure>
```

The patch:
```
-        if(content){
-            e.target.innerHTML = content;
+        if(content){
+            e.target.innerHTML = content + e.target.innerHTML;
```
