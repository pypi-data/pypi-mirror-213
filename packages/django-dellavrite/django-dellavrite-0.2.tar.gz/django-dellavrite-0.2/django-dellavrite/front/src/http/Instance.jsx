const host = 'http://api-shop.alabuga.space/api-shop/'
export const Instance = (url, method, token=null, body=null) =>
    fetch(host+url, {
        method: method,
        headers: {
            'Content-Type': "application/json",
            "Authorization": token && `Bearer ${token}`
        },
        body: body && JSON.stringify(body)
    })