window.script_name = [
    'zhihu_collection',
    'zhihu_zhuanlan',
    'zhihu_answers',
    'guoke_scientific',
    'qdaily',
    'jianshu_wenji',
    'jianshu_zhuanti',
    'jianshu_user',
    'zhihu_daily',
    'config'
];

window.kw =
    {
        zhihu_collection: [
            {name: 'window', default: 50, select: null}],
        zhihu_zhuanlan: [
            {name: 'window', default: 50, select: null}],
        zhihu_answers: [
            {name: 'window', default: 50, select: null}],
        guoke_scientific: [
            {name: 'window', default: 50, select: null}],
        qdaily: [
            {name: 'window', default: 50, select: null}],
        zhihu_daily: [
            {name: 'window', default: 50, select: null}],
        jianshu_wenji: [
            {name: 'window', default: 50, select: null},
            {name: 'order_by', default: 'seq', select: ['seq', 'commented_at', 'added_at']}],
        jianshu_zhuanti: [
            {name: 'window', default: 50, select: null},
            {name: 'order_by', default: 'top', select: ['top', 'commented_at', 'added_at']}],
        jianshu_user: [
            {name: 'window', default: 50, select: null},
            {name: 'order_by', default: 'top', select: ['top', 'commented_at', 'added_at']}],
    };