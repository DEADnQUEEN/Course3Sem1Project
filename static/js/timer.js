let intervals = {};

function timer(object, before=() => {}, after=() => {}) {
    before()
    if (object.id in intervals){
        clearTimeout(intervals[object.id])
    }
    intervals[object.id] = setTimeout(
        () => { after(); },
        3000
    )
}
