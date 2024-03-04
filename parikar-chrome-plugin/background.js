

chrome.action.onClicked.addListener((tab) => {
  if (!tab.url.includes('chrome://')) {
	var new_url = "https://www.parikar.org/play/instant/?url="+tab.url;
	chrome.tabs.create({ url: new_url });
  }
});

