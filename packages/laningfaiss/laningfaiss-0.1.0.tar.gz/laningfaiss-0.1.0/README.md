# Laning Faiss

### Example

```python
import asyncio
import laningfaiss

faiss = laningfaiss.Router("http://faiss-svc:8000")


async def main():
    ntotal = await faiss.ntotal()
    print(ntotal)
    # Output: 16

    search_res = await faiss.range_search([...], 0.8)
    print(search_res)
    # Output: [[1, 0.8587932], [2, 0.999999]]


if __name__ == '__main__':
    asyncio.run(main())

```


### Install From GitLab

```bash
pip install laningfaiss==0.0.12 --index-url http://__token__:sT2KnzLCX7avQ9t1MeA1@git.dev.laningtech.net/api/v4/projects/669/packages/pypi/simple
```
