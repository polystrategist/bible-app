import { Request, Response } from 'express';

export default {
    get: function (req: Request, res: Response) {
        res.send({
            "bibles": [1,2,3,4]
        })
    }
}