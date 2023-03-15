import crypto from 'node:crypto';

export function verifyWebhookSignature(
  rawBody: string | Buffer,
  signatureHeader: string | undefined,
  secret: string
): boolean {
  if (!signatureHeader || !secret) {
    return false;
  }

  const parts = signatureHeader.split('=');
  if (parts.length !== 2 || parts[0] !== 'sha256') {
    return false;
  }

  const providedHex = parts[1];
  const expectedHex = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');

  const providedBuf = Buffer.from(providedHex, 'hex');
  const expectedBuf = Buffer.from(expectedHex, 'hex');

  if (providedBuf.length !== expectedBuf.length) {
    return false;
  }

  return crypto.timingSafeEqual(providedBuf, expectedBuf);
}
