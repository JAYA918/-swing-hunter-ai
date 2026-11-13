SWING HUNTER AI – AUTOMATIC SCANNER (STARTER PACKAGE)

हे तयार केलेले iPhone-friendly PWA + automatic daily scanner आहे.
महत्त्वाचे: हा deploy-ready starter आहे; तुमच्या GitHub/hosting वर publish केल्यावरच
automatic report सुरू होईल. मी तुमच्या account मध्ये login/deploy करू शकत नाही.

सुरुवातीला:
1) GitHub वर मोफत account तयार करा: https://github.com
2) New repository तयार करा. नाव: swing-hunter-ai
3) या ZIP मधील सर्व files repository मध्ये upload करा (फोल्डर structure तसाच ठेवा).
4) Repository > Settings > Pages > Build and deployment > Source: Deploy from a branch
   Branch: main, Folder: /(root), Save.
5) Actions tab उघडा. Workflow ला परवानगी विचारल्यास enable करा.
6) Actions > Update Swing Hunter scan > Run workflow एकदा manually चालवा.
7) काही मिनिटांनी data/latest.json तयार होईल. Pages URL उघडून iPhone Safari >
   Share > Add to Home Screen करा.

वेळ:
- सकाळी 9:00 IST (सोमवार-शुक्रवार): मागील उपलब्ध daily candle.
- संध्याकाळी 6:00 IST (सोमवार-शुक्रवार): त्या दिवसाचा data उपलब्ध असल्यास.
GitHub scheduled jobs काही वेळा उशिरा चालू शकतात; exact minute guarantee नाही.

F&O UNIVERSE:
fno_symbols.txt मध्ये सुरुवातीला काही निवडक symbols दिले आहेत. पूर्ण NSE F&O
universe साठी ही यादी अधिकृत सध्याच्या यादीशी पडताळून अपडेट करा. Expired/removed
contracts असलेले symbols काढा.

DATA / LIMITATIONS:
- Scanner Yahoo Finance public data (yfinance) वापरतो. हे unofficial free feed आहे;
  availability, accuracy, delay किंवा symbols बदलू शकतात. NSE official feed नाही.
- हा prototype daily OHLCV वर आधारित आहे. 1-hour confirmation नाही.
- CE/PE म्हणजे underlying stock direction watch. Option strike, expiry, IV, option
  premium, liquidity किंवा premium-based SL/targets यातून मिळत नाहीत.
- Stop/Targets हे underlying stock च्या अंदाजित price levels आहेत; option premium levels नाहीत.
- Score heuristic आहे, backtested/guaranteed strategy नाही. Trade करण्यापूर्वी स्वतः
  chart, option chain, liquidity, expiry आणि risk तपासा.
- GitHub Actions free usage limits/policies बदलू शकतात.
- कोणतीही खरेदी/विक्री स्वयंचलितपणे होत नाही.

CSV manually upload करायची गरज नाही. GitHub Actions scheduled workflow डेटा घेऊन
report तयार करतो. App उघडल्यावर Refresh करा.
