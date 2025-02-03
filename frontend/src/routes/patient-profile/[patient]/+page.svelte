<script lang="ts">
	import { viewAsUser } from '$lib';
	import AnalysesList from '$lib/AnalysesList.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<svelte:head>
	<title>Patient Profile</title>
</svelte:head>

<div class="flex h-full border-t border-gray-300">
	<div
		class="flex-1 grow-[0.4] flex items-center justify-center border-r border-gray-300 overflow-x-hidden overflow-y-auto h-[90vh] pl-3 pr-2 "
	>
		<div class="container h-full mx-auto flex justify-center items-center">
			<div class="space-y-4 text-center flex flex-col items-center">
				<div class="flex justify-center space-x-2 flex-col">
					<label class="label">
						<span>Username</span>
						<input
							class="input"
							type="text"
							name="username"
							value={data.patient?.username}
							disabled
						/>
					</label>

					<label class="label">
						<span>Email</span>
						<input class="input" type="text" name="email" value={data?.patient?.email} disabled />
					</label>

					<label class="label">
						<span>First Name</span>
						<input
							class="input"
							type="text"
							name="first_name"
							value={data?.patient?.first_name}
							disabled
						/>
					</label>

					<label class="label">
						<span>Last Name</span>
						<input
							class="input"
							type="text"
							name="last_name"
							value={data?.patient?.last_name}
							disabled
						/>
					</label>

					<label class="label">
						<span>Height</span>
						<input class="input" type="text" name="height" value={data?.patient?.height} disabled />
					</label>

					<label class="label">
						<span>Weight</span>
						<input class="input" type="text" name="weight" value={data?.patient?.weight} disabled />
					</label>

					<label class="label">
						<span>Phone Number</span>
						<input
							class="input"
							type="tel"
							name="phone_number"
							value={data?.patient?.phone_number}
							disabled
						/>
					</label>

					<label class="label">
						<span>Birth Date</span>
						<input
							class="input"
							type="date"
							name="birth_date"
							value={data?.patient?.birth_date}
							disabled
						/>
					</label>
				</div>
			</div>
		</div>
	</div>

	<div class="flex-1 flex items-start justify-center w-full table-container ">
		<AnalysesList viewAsUser={$viewAsUser} />
	</div>
</div>
