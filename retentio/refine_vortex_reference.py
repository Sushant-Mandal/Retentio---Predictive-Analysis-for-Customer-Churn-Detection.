from pathlib import Path

path = Path('/home/ubuntu/retentio/client/src/components/BackgroundSystems.tsx')
text = path.read_text()
needle = '</svg></div><div className="portal-cursor-halo"/>'
trails = '''<path d="M270 32 C360 4 452 45 483 116 C512 183 469 226 495 294 C522 367 461 451 375 480 C303 505 260 541 194 508 C135 477 105 411 128 350 C150 292 110 238 141 172 C167 116 213 55 270 32 Z" className="portal-ribbon-trail trail-one"/><path d="M311 56 C374 34 435 67 462 126 C487 181 455 224 476 284 C496 342 451 410 384 438 C322 464 276 493 218 470 C171 451 145 397 162 345 C182 283 147 251 170 191 C193 128 249 72 311 56 Z" className="portal-ribbon-trail trail-two"/><path d="M255 70 C315 49 376 77 399 129 C419 178 391 215 414 269 C437 323 398 385 337 410 C280 434 239 455 197 429 C157 404 145 356 160 313 C177 261 150 223 172 177 C190 129 215 88 255 70 Z" className="portal-ribbon-trail trail-three"/><path d="M358 31 C427 35 486 78 501 135 C514 188 477 229 502 284 C523 333 500 384 461 417" className="portal-ribbon-trail trail-four"/></svg></div><div className="portal-cursor-halo"/>'''
if needle not in text:
    raise SystemExit('vortex svg close not found')
path.write_text(text.replace(needle, trails, 1))
