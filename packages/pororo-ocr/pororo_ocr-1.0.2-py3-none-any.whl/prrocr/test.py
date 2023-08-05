from prrocr import PororoOCR
ocr = PororoOCR(lang="ko")
result = ocr("https://lh3.googleusercontent.com/proxy/u0cVmJsmGQ9QF5pTuHaf1cnA2_XUmy4YL6lzzF_9177TBe2qXwjGugdly42dec5oI46Ks8sAFEtDU8bSTI4o4y7kWcQkXvLUGwpN00Ym7Eiendcj")
print(result)