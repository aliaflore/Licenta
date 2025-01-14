import type { Error, RadiographyPDFResult } from '$lib/types';
import type { State } from '@vincjo/datatables/server';

type result = RadiographyPDFResult & Error;

export const reload = async (state: State) => {
	const response = await fetch(
        `/api/radiography-pdf/?${getParams(state)}`, 
        {
            method: 'GET',
        }
    )
	const json = await response.json() as result;
    if(json.error) {
        return []
    }

    state.setTotalRows(json.count);
    return json.results;
};

const getParams = (state: State) => {
	const { rowsPerPage, sort, offset } = state;

	let params = `offset=${offset}`;

	if (rowsPerPage) {
		params += `&limit=${rowsPerPage}`;
	}

    if(sort) {
        params += `&ordering=${sort.direction === 'asc' ? '-' : ''}${sort.field?.toString()}`;
    }

	return params;
};
