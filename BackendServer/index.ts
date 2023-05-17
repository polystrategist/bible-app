import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import bibles from './routes/v1/bibles';

dotenv.config();

// const app: Express = express();
const port = process.env.PORT;
const verbose = process.env.NODE_ENV !== 'test'
const app = module.exports = express();

app.map = function(a: { [x: string]: any; }, route: string){
    route = route || '';
    for (const key in a) {
        switch (typeof a[key]) {
            // { '/path': { ... }}
            case 'object':
                app.map(a[key], route + key);
                break;
            // get: function(){ ... }
            case 'function':
                if (verbose) console.log('%s %s', key, route);
                // @ts-ignore
                app[key](route, a[key]);
                break;
        }
    }
};

app.get('/', (req: Request, res: Response) => {
    res.send('Express + TypeScript Server');
});

app.map({
    '/bibles': {
        get: bibles.get
    }
})

app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});