import { verifyWebhookSignature } from './hmac-signature-verifier.ts';

export interface OrderWebhookEvent {
  eventId: string;
  orderId: string;
  amountCents: number;
}

export function handleIncomingOrderWebhook(
  rawBody: string,
  signatureHeader: string | undefined,
  webhookSecret: string
): { accepted: boolean; orderId?: string } {
  const isValid = verifyWebhookSignature(rawBody, signatureHeader, webhookSecret);
  if (!isValid) {
    return { accepted: false };
  }

  const parsed = JSON.parse(rawBody) as OrderWebhookEvent;
  return {
    accepted: true,
    orderId: parsed.orderId,
  };
}
