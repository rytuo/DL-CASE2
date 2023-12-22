export interface Result {
    texts: string[],
}


export default {
    get_vacancies_by_cv: async function(text: string) {
        const res = await fetch("http://0.0.0.0:8000/api/v1/models/:cv", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data: text,
            }),
        });
        if (res.status === 200) {
            const json = await res.json();
            return json as Result;
        }
        throw new Error(`Error: ${res.statusText}`);
    },

    get_cvs_by_vacancy: async function(text: string) {
        const res = await fetch("http://0.0.0.0:8000/api/v1/models/:vancancy", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data: text,
            }),
        });
        if (res.status === 200) {
            const json = await res.json();
            return json as Result;
        }
        throw new Error(`Error: ${res.statusText}`);
    },
};
