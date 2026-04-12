df['Week'] = df['Date'].dt.isocalendar().week
df['Month'] = df['Date'].dt.month
weekly = df.groupby('Week').sum()
monthly = df.groupby('Month').sum()
