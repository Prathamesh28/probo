const axios = require("axios");
const buy = () => {
  // BUY YES API
  //   fetch("https://prod.api.probo.in/api/v1/oms/order/initiate", {
  //     headers: {
  //       accept: "*/*",
  //       "accept-language": "en",
  //       appid: "in.probo.pro",
  //       authorization: "Bearer E62wjcYhBaP+6jF1sjXeA55QEp/HbkgjfVMzRupq0AE=",
  //       "content-type": "application/json",
  //       "sec-ch-ua":
  //         '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  //       "sec-ch-ua-mobile": "?0",
  //       "sec-ch-ua-platform": '"macOS"',
  //       "sec-fetch-dest": "empty",
  //       "sec-fetch-mode": "cors",
  //       "sec-fetch-site": "same-site",
  //       "x-device-os": "ANDROID",
  //       "x-version-name": "10",
  //       Referer: "https://trading.probo.in/",
  //       "Referrer-Policy": "strict-origin-when-cross-origin",
  //     },
  //     body: '{"event_id":1571043,"offer_type":"buy","order_type":"LO","l1_order_quantity":1,"l1_expected_price":"0.5"}',
  //     method: "POST",
  //   }).then((res) => {
  //     console.log(res);
  //   });

  //BUY NO API
  //   fetch("https://prod.api.probo.in/api/v1/oms/order/initiate", {
  //     headers: {
  //       accept: "*/*",
  //       "accept-language": "en",
  //       appid: "in.probo.pro",
  //       authorization: "Bearer E62wjcYhBaP+6jF1sjXeA55QEp/HbkgjfVMzRupq0AE=",
  //       "content-type": "application/json",
  //       "sec-ch-ua":
  //         '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  //       "sec-ch-ua-mobile": "?0",
  //       "sec-ch-ua-platform": '"macOS"',
  //       "sec-fetch-dest": "empty",
  //       "sec-fetch-mode": "cors",
  //       "sec-fetch-site": "same-site",
  //       "x-device-os": "ANDROID",
  //       "x-version-name": "10",
  //       Referer: "https://trading.probo.in/",
  //       "Referrer-Policy": "strict-origin-when-cross-origin",
  //     },
  //     body: '{"event_id":1571043,"offer_type":"sell","order_type":"LO","l1_order_quantity":1,"l1_expected_price":"0.5"}',
  //     method: "POST",
  //   }).then((res) => {
  //     console.log(res);
  //   });

  // Exit API
  //   fetch("https://prod.api.probo.in/api/v2/oms/order/exit", {
  //     "headers": {
  //       "accept": "*/*",
  //       "accept-language": "en",
  //       "appid": "in.probo.pro",
  //       "authorization": "Bearer E62wjcYhBaP+6jF1sjXeA55QEp/HbkgjfVMzRupq0AE=",
  //       "content-type": "application/json",
  //       "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
  //       "sec-ch-ua-mobile": "?0",
  //       "sec-ch-ua-platform": "\"macOS\"",
  //       "sec-fetch-dest": "empty",
  //       "sec-fetch-mode": "cors",
  //       "sec-fetch-site": "same-site",
  //       "x-device-os": "ANDROID",
  //       "x-version-name": "10",
  //       "Referer": "https://trading.probo.in/",
  //       "Referrer-Policy": "strict-origin-when-cross-origin"
  //     },
  //     "body": "{\"exit_params\":[{\"exit_price\":0.5,\"order_id\":533288443}]}",
  //     "method": "PUT"
  //   });

  // GET BEST PRICES API
  fetch(
    "https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId=1571110&requestType=availableQuantities",
    {
      headers: {
        accept: "*/*",
        "accept-language": "en",
        appid: "in.probo.pro",
        authorization: "Bearer E62wjcYhBaP+6jF1sjXeA55QEp/HbkgjfVMzRupq0AE=",
        "content-type": "application/json",
        "if-none-match": 'W/"1dc-49s8qxPCRRgsuJrYjhkK6G2cVKQ"',
        "sec-ch-ua":
          '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
        Referer: "https://trading.probo.in/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
      },
      body: null,
      method: "GET",
    }
  ).then((res) => {
    console.log(res.body);
  });
};
// buy();

const youtubeLiveViewCount = async () => {
  // https://developers.google.com/youtube/v3/docs/videos/list?apix=true#parameters

  const youtubeBroadcastId = "3mchJ-EW9rM";
  const youtubeAccessToken = "AIzaSyA5agtIvha5x2gEMiuo-TkFpZ8msaUBkB4";

  let viewCount = await axios
    .get(
      `https://youtube.googleapis.com/youtube/v3/videos?part=statistics%2C%20status&id=${youtubeBroadcastId}&key=AIzaSyA5agtIvha5x2gEMiuo-TkFpZ8msaUBkB4`,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    .then((res) => {
      console.log(res.data.items[0].statistics.viewCount);
      return res.data.items[0].statistics.viewCount;
    })
    .catch((err) => {
      console.log(err);
    });
};
youtubeLiveViewCount();

