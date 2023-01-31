# LibreOffice Tricks

## Auto incrementing Image URL values in LibreOffice
1. Go to cell you want to copy URLs of (in our case, Image URLs, which is U8 for us)
2. In an empty column in the same row (in our case, V8), add the card number (for us, 6, since we're starting on WTR6)
3. Go to the next empty column in the same row (in our case, W8), and copy\paste this formula in
    ```=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE($X$8,"WTR006",CONCATENATE("WTR", TEXT(Y8, "000"))),"WTR6",CONCATENATE("WTR", Y8)),"WTR_6",CONCATENATE("WTR_", Y8))```
4. Replace the WTR006, WTR6, WTR_6 values in the formula with the set number you're trying to increment, and replace the instances of $U$8 and V8 with your cell values
5. Drag copy the cells - you should see your formula cell have the proper URLs!
6. Highlight and copy the new cells from the column you generated with formulas
7. Highlight the actual cells you want the URLs in (since they're all copies of the original URL right now)
8. Right click, select Paste Special > Paste Special..., and click Values Only
9. Delete your temporary columns, and you're done!
10. Note: You can use something like this for Variations: `SUBSTITUTE($W$8,"WTR006",CONCATENATE("WTR", TEXT(Y8, "000")))`