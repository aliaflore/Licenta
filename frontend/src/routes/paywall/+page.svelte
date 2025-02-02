<script lang="ts">
	import { checkout } from '$lib/stripe';

	function handleCheckout() {
		checkout();
	}
</script>

<div class="flex flex-col items-center justify-center min-h-screen p-6">
	<div class="shadow-md rounded-lg p-6 max-w-md w-full">
		<h2 class="text-2xl font-bold mb-4">Subscribe for 20 RON/month</h2>
		<p class="mb-4">With your subscription, you get:</p>
		<ul class="list-disc list-inside mb-4">
			<li>Access to the platform</li>
			<li>A way to store and analyze all of your analyses and radiographies</li>
			<li>A platform where the doctors are able to send you suggestions for you to follow</li>
		</ul>
		<button
			class="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700"
			on:click={handleCheckout}
		>
			Subscribe Now
		</button>
	</div>
</div>
