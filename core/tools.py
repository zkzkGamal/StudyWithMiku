from tools.network import network, openwifi, searchweb
from tools.embedded import embedded_pdf
from tools.browser import open_browser
from tools.processes_tools import findProcess , killProcess

__all__ = [
    network.check_internet,
    openwifi.enable_wifi,
    searchweb.duckduckgo_search,
    embedded_pdf.embedded_pdf,
    open_browser.open_browser,
    findProcess.find_process,
    killProcess.kill_process,
]