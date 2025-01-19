import {
	writable
} from 'svelte/store';
import type { User } from './types';


export const viewAsUser = writable<User|null>(null);
