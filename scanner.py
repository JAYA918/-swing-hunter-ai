import yfinance as yf
import pandas as pd
import numpy as np
import json, datetime, pathlib, time

ROOT=pathlib.Path(__file__).parent
symbols=[x.strip() for x in (ROOT/"fno_symbols.txt").read_text().splitlines() if x.strip() and not x.startswith("#")]

def rsi(s,n=14):
    d=s.diff(); up=d.clip(lower=0).ewm(alpha=1/n,adjust=False).mean()
    dn=(-d.clip(upper=0)).ewm(alpha=1/n,adjust=False).mean()
    return 100-(100/(1+up/dn.replace(0,np.nan)))

def scan(sym):
    df=yf.download(sym+".NS",period="9mo",interval="1d",auto_adjust=True,progress=False,threads=False)
    if df is None or len(df)<60:return None
    if isinstance(df.columns,pd.MultiIndex): df.columns=df.columns.get_level_values(0)
    df=df.dropna()
    c=df["Close"]; h=df["High"]; l=df["Low"]; v=df["Volume"]
    e20=c.ewm(span=20,adjust=False).mean(); e50=c.ewm(span=50,adjust=False).mean()
    rv=rsi(c); tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=tr.rolling(14).mean(); av=v.rolling(20).mean()
    last=float(c.iloc[-1]); R=float(rv.iloc[-1]); E20=float(e20.iloc[-1]); E50=float(e50.iloc[-1])
    vr=float(v.iloc[-1]/av.iloc[-1]) if av.iloc[-1] else 0
    prior_high=float(h.iloc[-21:-1].max()); prior_low=float(l.iloc[-21:-1].min())
    atrv=float(atr.iloc[-1]); atrprev=float(atr.iloc[-6:-1].mean())
    uptrend=last>E20>E50; downtrend=last<E20<E50
    breakout=last>prior_high; breakdown=last<prior_low
    score=0; reasons=[]
    if uptrend: score+=25; reasons.append("EMA bullish")
    elif downtrend: score+=25; reasons.append("EMA bearish")
    if uptrend and 45<=R<=68: score+=15; reasons.append("RSI bullish zone")
    elif downtrend and 32<=R<=55: score+=15; reasons.append("RSI bearish zone")
    if vr>=1.5: score+=20; reasons.append("Volume expansion")
    elif vr>=1.15: score+=10; reasons.append("Volume above average")
    if breakout or breakdown: score+=20; reasons.append("20-day range break")
    if atrv>atrprev: score+=10; reasons.append("ATR expanding")
    if 45<=R<=60: score+=10; reasons.append("RSI balanced")
    signal="WAIT"
    if score>=65 and uptrend and (breakout or vr>=1.5) and R<72: signal="CE"
    if score>=65 and downtrend and (breakdown or vr>=1.5) and R>28: signal="PE"
    # Underlying reference levels, not option-premium levels.
    stop=last-1.2*atrv if signal=="CE" else last+1.2*atrv
    t1=last+1.5*atrv if signal=="CE" else last-1.5*atrv
    t2=last+2.5*atrv if signal=="CE" else last-2.5*atrv
    return {"symbol":sym,"signal":signal,"score":int(min(score,100)),"close":round(last,2),"rsi":round(R,1),
            "ema20":round(E20,2),"ema50":round(E50,2),"volume_ratio":round(vr,2),
            "stop":round(stop,2),"t1":round(t1,2),"t2":round(t2,2),"reasons":reasons,
            "data_date":str(df.index[-1].date())}

def main():
    out=[]
    for s in symbols:
        try:
            x=scan(s)
            if x: out.append(x)
        except Exception as e: print("Skipped",s,str(e)[:100])
        time.sleep(.15)
    out.sort(key=lambda x:x["score"],reverse=True)
    dates=[x["data_date"] for x in out]
    report={"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "data_through":max(dates) if dates else None,"universe_count":len(out),
            "top5":out[:5]}
    (ROOT/"data"/"latest.json").write_text(json.dumps(report,indent=2))
    print("Report generated:",len(out),"symbols")
if __name__=="__main__": main()
