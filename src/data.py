import numpy as np

def make_loading_case(seed, tones=64, taps=8, noise_var=0.1, pilots=20):
    rng = np.random.default_rng(seed)

    power = np.exp(-np.arange(taps)/2.0)
    power /= power.sum()

    channel_taps = np.sqrt(power / 2) * (rng.normal(size=taps) + 1j * rng.normal(size=taps))
    h = np.fft.fft(channel_taps, n=tones)

    noise = np.sqrt(noise_var / 2) * (rng.normal(size=(pilots,tones)) + 1j * rng.normal(size=(pilots,tones)))

    h_hat = (h[None, :] + noise).mean(axis=0)

    noise_only = np.sqrt(noise_var / 2) * (rng.normal(size=(pilots, tones)) + 1j * rng.normal(size=(pilots, tones)))

    variance_hat = np.mean(np.abs(noise_only) ** 2, axis=0)

    g_true = np.abs(h) ** 2 / noise_var

    g_hat = np.abs(h_hat) ** 2 / np.maximum(variance_hat, 1e-12)

    return g_true, np.maximum(g_hat, 1e-12)

if __name__ == "__main__":
    g_true, g_hat = make_loading_case(seed=0)

    assert g_true.shape == (64,)
    assert g_hat.shape == (64,)

    assert np.all(np.isfinite(g_true))
    assert np.all(np.isfinite(g_hat))

    assert np.all(g_true >= 0)
    assert np.all(g_hat > 0)

    repeat_true, repeat_hat = make_loading_case(seed=0)

    assert np.array_equal(g_true, repeat_true)
    assert np.array_equal(g_hat, repeat_hat)

    print("True channel quality:", g_true[:5])
    print("Estimated channel quality:", g_hat[:5])
    print("Data checks passed.")