import type { PatientInviteResult, Error } from '$lib/types';
import type { State } from '@vincjo/datatables/server';

type result = PatientInviteResult & Error;

export const reload = async (state: State) => {
	const response = await fetch(
        `/api/doctor-invites/?${getParams(state)}`, 
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
	const { rowsPerPage, sort, offset, search } = state;

	let params = `offset=${offset}`;

	if (rowsPerPage) {
		params += `&limit=${rowsPerPage}`;
	}

    if(sort) {
        params += `&ordering=${sort.direction === 'asc' ? '-' : ''}${sort.field?.toString()}`;
    }

    if(search) {
        params += `&search=${search}`;
    }

	return params;
};
