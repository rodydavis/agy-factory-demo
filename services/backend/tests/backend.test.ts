import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { test } from 'node:test';
import { formatCurrencyWithTax, retryWithBackoff } from '../src/catalog-sync.ts';
import { handleIncomingOrderWebhook } from '../src/webhook-handler.ts';

test('formatCurrencyWithTax calculates subtotal + tax and formats USD', () => {
  const formatted = formatCurrencyWithTax(10000, 0.0825, 'USD');
  assert.equal(formatted, '$108.25');
});

test('retryWithBackoff retries transient failures and succeeds', async () => {
  let calls = 0;
  const result = await retryWithBackoff(
    async () => {
      calls += 1;
      if (calls < 2) throw new Error('Transient network failure');
      return 'ok';
    },
    3,
    5
  );
  assert.equal(result, 'ok');
  assert.equal(calls, 2);
});

test('handleIncomingOrderWebhook verifies RFC 2104 HMAC-SHA256 signatures', () => {
  const secret = 'whsec_test_secret';
  const payload = JSON.stringify({
    eventId: 'evt_1',
    orderId: 'ord_99',
    amountCents: 4500,
  });
  const validSig =
    'sha256=' + crypto.createHmac('sha256', secret).update(payload).digest('hex');

  const accepted = handleIncomingOrderWebhook(payload, validSig, secret);
  assert.equal(accepted.accepted, true);
  assert.equal(accepted.orderId, 'ord_99');

  const rejected = handleIncomingOrderWebhook(payload, 'sha256=deadbeef', secret);
  assert.equal(rejected.accepted, false);
});
