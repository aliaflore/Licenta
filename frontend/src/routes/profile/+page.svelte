<script lang="ts">
	import { enhance } from '$app/forms';
	import type { PageData, ActionData } from './$types';

	export let data: PageData;
	export let form: ActionData;
</script>

<svelte:head>
	<title>Profile</title>
</svelte:head>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-4 text-center flex flex-col items-center">
		<div class="flex justify-center space-x-2 flex-col">
			{#if form?.modified}
				<aside class="alert variant-ghost">
					<div class="alert-message">
						<h3 class="h3">Success!</h3>
						<p>The changes have been saved!</p>
					</div>
				</aside>
			{/if}
			{#if form?.deleted === false}
				<aside class="alert variant-ghost !bg-red-500">
					<div class="alert-message">
						<h3 class="h3">Error!</h3>
						<p>Could not delete your account!</p>
					</div>
				</aside>
			{/if}
			<form
				method="post"
				class="space-y-4"
				action="?/edit"
				use:enhance={() => {
					return async ({ update }) => {
						update({ reset: false });
					};
				}}
			>
				{#if form?.errors?.non_field_errors}
					<p class="text-red-500">{form.errors.non_field_errors}</p>
				{/if}
				<input type="hidden" name="pk" value={data?.user?.pk} />

				<label class="label">
					<span>Username</span>
					<input class="input" type="text" name="username" value={data?.user?.username} disabled />
				</label>

				<label class="label">
					<span>Email</span>
					<input class="input" type="text" name="email" value={data?.user?.email} disabled />
				</label>

				{#if form?.errors?.first_name}
					<p class="text-red-500">{form.errors.first_name}</p>
				{/if}
				<label class="label">
					<span>First Name</span>
					<input class="input" type="text" name="first_name" value={data?.user?.first_name} />
				</label>

				{#if form?.errors?.last_name}
					<p class="text-red-500">{form.errors.last_name}</p>
				{/if}
				<label class="label">
					<span>Last Name</span>
					<input class="input" type="text" name="last_name" value={data?.user?.last_name} />
				</label>

				{#if data?.user?.is_doctor}
					{#if form?.errors?.accept_new_patients}
						<p class="text-red-500">{form.errors.accept_new_patients}</p>
					{/if}
					<label class="label">
						<input
							class="checkbox"
							type="checkbox"
							name="birth_date"
							checked={data?.user?.accept_new_patients}
						/>
						<span>Accept New Patients</span>
					</label>
				{:else}
					{#if form?.errors?.height}
						<p class="text-red-500">{form.errors.height}</p>
					{/if}
					<label class="label">
						<span>Height</span>
						<input class="input" type="text" name="height" value={data?.user?.height} />
					</label>

					{#if form?.errors?.weight}
						<p class="text-red-500">{form.errors.weight}</p>
					{/if}
					<label class="label">
						<span>Weight</span>
						<input class="input" type="text" name="weight" value={data?.user?.weight} />
					</label>

					{#if form?.errors?.phone_number}
						<p class="text-red-500">{form.errors.phone_number}</p>
					{/if}
					<label class="label">
						<span>Phone Number</span>
						<input class="input" type="tel" name="phone_number" value={data?.user?.phone_number} />
					</label>

					{#if form?.errors?.birth_date}
						<p class="text-red-500">{form.errors.birth_date}</p>
					{/if}
					<label class="label">
						<span>Birth Date</span>
						<input class="input" type="date" name="birth_date" value={data?.user?.birth_date} />
					</label>
				{/if}

				{#if form?.errors?.password1}
					<p class="text-red-500">{form.errors.password1}</p>
				{/if}
				<label class="label">
					<span>Password</span>
					<input class="input" type="password" name="password1" />
				</label>

				{#if form?.errors?.password2}
					<p class="text-red-500">{form.errors.password2}</p>
				{/if}
				<label class="label">
					<span>Confirm Password</span>
					<input class="input" type="password" name="password2" />
				</label>

				<button class="w-full btn-md btn variant-filled" type="submit">Update Profile</button>
			</form>
		</div>
		<form method="post" action="?/delete" class="w-full">
			<input type="hidden" name="user_pk" value={data?.user?.pk} />
			<button class="w-full btn-md btn variant-ghost !bg-red-500" type="submit"
				>Delete Account</button
			>
		</form>
	</div>
</div>
