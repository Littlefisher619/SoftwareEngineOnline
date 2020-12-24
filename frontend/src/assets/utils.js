export function getUrlKey(name) {
    let href = decodeURIComponent(location.href)
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(href) || [, ""])[1].replace(/\+/g, '%20')) || null
}