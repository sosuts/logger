# with engine.connect() as conn:
#     # create tables if not exists
#     Base.metadata.create_all(conn)

# with Session(engine) as session:
#     session.add(User(full_name="John Doe"))
#     session.add(User(full_name="Jasmine"))
#     session.commit()


# with Session(engine) as session:
#     user = session.query(User).filter(User.full_name == "John Doe").one_or_none()
#     if user is None:
#         raise ValueError("User not found")
#     session.add(
#         Process(
#             name="Preparation",
#             type="pre",
#             created_by=user.id,
#             updated_by=user.id,
#         )
#     )
#     # user = session.query(User).filter(User.full_name == "Jasmine").first()
#     # session.add(
#     #     Reagent(name="Acetone", lot="123", created_by=user.id, updated_by=user.id)
#     # )
#     session.commit()

# # with Session(engine) as session:
# #     reagent = session.query(Reagent).filter(Reagent.lot == "123").first()
# #     reagent.updated_by = 100
# #     session.commit()

# with Session(engine) as session:
#     # print all table
#     for user in session.query(User).all():
#         print(user)
#     for reagent in session.query(Reagent).all():
#         print(1, reagent.created_by_user)
#     for process in session.query(Process).all():
#         print(process.updated_by_user)
