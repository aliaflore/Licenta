import type { AnalysisPDFResult, Error, User } from '$lib/types';
import type { State } from '@vincjo/datatables/server';

type result = AnalysisPDFResult & Error;

export const reload = async (state: State, viewAsUserState: User | null) => {
	const response = await fetch(
        `/api/analysis-pdf/?${getParams(state, viewAsUserState)}`, 
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

const getParams = (state: State, viewAsUserState: User | null) => {
	const { rowsPerPage, sort, offset } = state;

	let params = `offset=${offset}`;

	if (rowsPerPage) {
		params += `&limit=${rowsPerPage}`;
	}

    if(sort) {
        params += `&ordering=${sort.direction === 'asc' ? '-' : ''}${sort.field?.toString()}`;
    }

    if(viewAsUserState) {
        params += `&user=${viewAsUserState.pk}`;
    }

	return params;
};
