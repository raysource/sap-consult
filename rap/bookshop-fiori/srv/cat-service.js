const cds = require('@sap/cds');

module.exports = cds.service.impl(function () {

    const { Books } = this.entities;

    this.before(['CREATE', 'UPDATE'], Books, (req) => {

        const data = req.data;

        // タイトル必須
        if (!data.title) {
            req.error(400, 'Title is required.');
        }

        // 価格チェック
        if (data.price <= 0) {
            req.error(400, 'Price must be greater than 0.');
        }

        // 在庫チェック
        if (data.stock < 0) {
            req.error(400, 'Stock cannot be negative.');
        }

        // ステータス設定
        if (data.status == 0) {
            data.status = 'SoldOut';
        } else {
            data.status = 'Active';
        }

    });

    this.after(['CREATE', 'UPDATE'], Books, async (data, req) => {

        console.log(`${req.event} Book`);

        console.log(data.title);

    });

    this.on('Publish', Books, async(req)=>{

        const ID = req.params[0].ID;

        await UPDATE(Books)
            .set({
                status:'Published'
            })
            .where({ID});

        return SELECT.one.from(Books).where({ ID });

    });
});