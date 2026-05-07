import speedtest


def run_speedtest():
    st = speedtest.Speedtest(secure=True)
    st.get_best_server()

    download = st.download() / 1_000_000 
    upload = st.upload() / 1_000_000 
    ping = st.results.ping

    return {
        "download": round(download, 2),
        "upload": round(upload, 2),
        "ping": round(ping, 2)
    }